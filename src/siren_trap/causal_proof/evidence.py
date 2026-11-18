"""Event reconstruction and conservative action-effect evidence classification."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Iterable


class EffectLevel(str, Enum):
    """Highest independently evidenced stage of an attempted external action."""

    ATTEMPTED = "ATTEMPTED"
    DISPATCHED = "DISPATCHED"
    RECEIVED = "RECEIVED"
    EFFECT_CONFIRMED = "EFFECT_CONFIRMED"
    NOT_OBSERVED = "NOT_OBSERVED"


@dataclass(frozen=True)
class ActionEvidence:
    """Evidence-backed action lifecycle; later stages require earlier evidence."""

    action_id: str
    authorization_id: str
    source_id: str
    attempted: bool
    dispatched: bool
    receiver_received: bool
    effect_confirmed: bool

    def __post_init__(self) -> None:
        if not all((self.action_id, self.authorization_id, self.source_id)):
            raise ValueError("Action and provenance identifiers are required.")
        if self.dispatched and not self.attempted:
            raise ValueError("DISPATCHED evidence requires ATTEMPTED evidence.")
        if self.receiver_received and not self.dispatched:
            raise ValueError("RECEIVED evidence requires DISPATCHED evidence.")
        if self.effect_confirmed and not self.receiver_received:
            raise ValueError("EFFECT_CONFIRMED requires RECEIVED evidence.")

    @property
    def effect_level(self) -> EffectLevel:
        if self.effect_confirmed:
            return EffectLevel.EFFECT_CONFIRMED
        if self.receiver_received:
            return EffectLevel.RECEIVED
        if self.dispatched:
            return EffectLevel.DISPATCHED
        if self.attempted:
            return EffectLevel.ATTEMPTED
        return EffectLevel.NOT_OBSERVED

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["effect_level"] = self.effect_level.value
        return value


def reconstruct_events(events: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate and chronologically order JSONL-style events without inference."""
    normalized = []
    for event in events:
        if not isinstance(event, dict):
            raise TypeError("Every event must be a mapping.")
        event_id = event.get("event_id")
        timestamp = event.get("timestamp")
        event_type = event.get("event_type")
        details = event.get("details", {})
        if not all(isinstance(value, str) and value for value in (
            event_id, timestamp, event_type
        )):
            raise ValueError("Events require event_id, timestamp, and event_type.")
        if not isinstance(details, dict):
            raise ValueError("Event details must be a mapping.")
        try:
            parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("Event timestamp must be ISO-8601.") from exc
        normalized.append((parsed, {**event, "details": dict(details)}))
    normalized.sort(key=lambda item: (item[0], item[1]["event_id"]))
    return [item[1] for item in normalized]


def correlate_action_events(
    events: Iterable[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Group explicit authorization/source/action identifiers by action ID."""
    correlations: dict[str, dict[str, Any]] = {}
    for event in reconstruct_events(events):
        details = event["details"]
        action_id = details.get("action_id")
        if not isinstance(action_id, str) or not action_id:
            continue
        record = correlations.setdefault(
            action_id,
            {"authorization_ids": set(), "source_ids": set(), "event_ids": []},
        )
        for field, key in (
            ("authorization_id", "authorization_ids"),
            ("source_id", "source_ids"),
        ):
            value = details.get(field)
            if isinstance(value, str) and value:
                record[key].add(value)
        record["event_ids"].append(event["event_id"])
    return {
        action_id: {
            "authorization_ids": sorted(value["authorization_ids"]),
            "source_ids": sorted(value["source_ids"]),
            "event_ids": value["event_ids"],
        }
        for action_id, value in correlations.items()
    }
