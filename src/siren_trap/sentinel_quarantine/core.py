"""Fail-closed orchestration for an out-of-process enforcement adapter.

This module coordinates enforcement; it does not itself create OS namespaces,
firewall rules, or process boundaries. A deployment must inject a trusted
control-plane adapter that performs those operations outside the agent process.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from enum import Enum
from threading import RLock
from typing import Protocol

from siren_trap.telemetry.event_logger import JsonlEventLogger


class TriggerReason(str, Enum):
    """Events that require immediate session containment."""

    LURE_INTERACTION = "LURE_INTERACTION"
    AUTHORIZATION_VIOLATION = "AUTHORIZATION_VIOLATION"


class ContainmentStatus(str, Enum):
    """Aggregate status across all required enforcement controls."""

    CONTAINED = "CONTAINED"
    PARTIALLY_CONTAINED = "PARTIALLY_CONTAINED"


class EnforcementAdapter(Protocol):
    """Trusted external control plane; methods must enforce outside the agent."""

    def revoke_session(self, session_id: str) -> bool: ...

    def block_egress(self, session_id: str) -> bool: ...

    def contain_children(self, session_id: str) -> bool: ...

    def isolate_session(self, session_id: str) -> bool: ...


@dataclass(frozen=True)
class EnforcementResult:
    """Auditable outcome of a containment attempt."""

    session_id: str
    trigger: str
    status: ContainmentStatus
    controls: dict[str, bool]
    errors: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["status"] = self.status.value
        return value


class SentinelQuarantine:
    """Coordinate immediate, idempotent enforcement through an external adapter.

    A session is marked CONTAINED only when session revocation, egress blocking,
    delegated-child containment, and quarantine isolation all report success.
    Missing or failing controls produce PARTIALLY_CONTAINED, never a false pass.
    """

    _SESSION_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    _CONTROLS = (
        ("session_revoked", "revoke_session"),
        ("egress_blocked", "block_egress"),
        ("child_sessions_contained", "contain_children"),
        ("quarantine_boundary_applied", "isolate_session"),
    )

    def __init__(
        self,
        adapter: EnforcementAdapter,
        *,
        event_logger: JsonlEventLogger,
    ) -> None:
        self._adapter = adapter
        self._event_logger = event_logger
        self._lock = RLock()
        self._results: dict[str, EnforcementResult] = {}

    def contain(
        self, session_id: str, trigger: TriggerReason
    ) -> EnforcementResult:
        """Apply every external control once and persist the resulting state."""
        if not isinstance(session_id, str) or not self._SESSION_ID.fullmatch(session_id):
            raise ValueError("session_id must be a bounded opaque identifier.")
        if not isinstance(trigger, TriggerReason):
            raise TypeError("trigger must be a TriggerReason.")

        with self._lock:
            existing = self._results.get(session_id)
            if existing is not None:
                return existing

            controls: dict[str, bool] = {}
            errors: dict[str, str] = {}
            # Revocation is first; all remaining controls are attempted even if
            # one adapter operation fails, to maximize defensive coverage.
            for result_key, method_name in self._CONTROLS:
                try:
                    outcome = getattr(self._adapter, method_name)(session_id)
                    controls[result_key] = outcome is True
                    if outcome is not True:
                        errors[result_key] = "CONTROL_NOT_CONFIRMED"
                except Exception as exc:  # adapter boundary: convert failure to partial
                    controls[result_key] = False
                    errors[result_key] = type(exc).__name__

            status = (
                ContainmentStatus.CONTAINED
                if all(controls.values())
                else ContainmentStatus.PARTIALLY_CONTAINED
            )
            result = EnforcementResult(
                session_id=session_id,
                trigger=trigger.value,
                status=status,
                controls=controls,
                errors=errors,
            )
            self._event_logger.record("SENTINEL_CONTAINMENT_RESULT", result.to_dict())
            self._results[session_id] = result
            return result

    def on_lure_interaction(self, session_id: str) -> EnforcementResult:
        """Contain the session immediately after a trusted lure-access signal."""
        return self.contain(session_id, TriggerReason.LURE_INTERACTION)

    def on_authorization_violation(self, session_id: str) -> EnforcementResult:
        """Contain the session immediately after a policy-engine violation."""
        return self.contain(session_id, TriggerReason.AUTHORIZATION_VIOLATION)

    def get_status(self, session_id: str) -> EnforcementResult | None:
        """Return the last recorded local result; no enforcement is implied."""
        with self._lock:
            return self._results.get(session_id)
