from siren_trap.sentinel_quarantine import (
    ContainmentStatus,
    EnforcementResult,
    SentinelQuarantine,
    TriggerReason,
)


class FakeEnforcer:
    def __init__(self, *, revoke=True, egress=True, children=True, isolate=True):
        self.revoke = revoke
        self.egress = egress
        self.children = children
        self.isolate = isolate
        self.calls = []

    def revoke_session(self, session_id):
        self.calls.append(("revoke", session_id))
        return self.revoke

    def block_egress(self, session_id):
        self.calls.append(("egress", session_id))
        return self.egress

    def contain_children(self, session_id):
        self.calls.append(("children", session_id))
        return self.children

    def isolate_session(self, session_id):
        self.calls.append(("isolate", session_id))
        return self.isolate


def test_quarantine_requires_every_external_enforcement_control(tmp_path):
    enforcer = FakeEnforcer()
    sentinel = SentinelQuarantine(enforcer, event_log_path=tmp_path / "events.jsonl")

    result = sentinel.contain("session-1", TriggerReason.LURE_INTERACTION)

    assert result.status is ContainmentStatus.CONTAINED
    assert result.controls == {
        "session_revoked": True,
        "egress_blocked": True,
        "child_sessions_contained": True,
        "quarantine_boundary_applied": True,
    }
    assert [call[0] for call in enforcer.calls] == [
        "revoke", "egress", "children", "isolate"
    ]


def test_missing_egress_control_is_only_partially_contained(tmp_path):
    sentinel = SentinelQuarantine(
        FakeEnforcer(egress=False), event_log_path=tmp_path / "events.jsonl"
    )

    result = sentinel.contain("session-2", TriggerReason.AUTHORIZATION_VIOLATION)

    assert result.status is ContainmentStatus.PARTIALLY_CONTAINED
    assert result.controls["egress_blocked"] is False


def test_exception_from_control_fails_closed_and_records_partial_state(tmp_path):
    class Broken(FakeEnforcer):
        def block_egress(self, session_id):
            raise OSError("firewall adapter unavailable")

    sentinel = SentinelQuarantine(Broken(), event_log_path=tmp_path / "events.jsonl")
    result = sentinel.contain("session-3", TriggerReason.LURE_INTERACTION)

    assert result.status is ContainmentStatus.PARTIALLY_CONTAINED
    assert result.controls["egress_blocked"] is False
    assert result.errors["egress_blocked"] == "OSError"


def test_repeat_trigger_returns_existing_containment_result(tmp_path):
    enforcer = FakeEnforcer()
    sentinel = SentinelQuarantine(enforcer, event_log_path=tmp_path / "events.jsonl")

    first = sentinel.contain("session-4", TriggerReason.LURE_INTERACTION)
    second = sentinel.contain("session-4", TriggerReason.AUTHORIZATION_VIOLATION)

    assert second == first
    assert len(enforcer.calls) == 4


def test_child_sessions_are_part_of_containment_decision(tmp_path):
    sentinel = SentinelQuarantine(
        FakeEnforcer(children=False), event_log_path=tmp_path / "events.jsonl"
    )

    result = sentinel.contain("session-5", TriggerReason.LURE_INTERACTION)

    assert result.status is ContainmentStatus.PARTIALLY_CONTAINED
    assert result.controls["child_sessions_contained"] is False


def test_invalid_session_identifier_is_rejected(tmp_path):
    sentinel = SentinelQuarantine(
        FakeEnforcer(), event_log_path=tmp_path / "events.jsonl"
    )

    import pytest

    with pytest.raises(ValueError):
        sentinel.contain("../session", TriggerReason.LURE_INTERACTION)
