from siren_trap.causal_proof import (
    ActionEvidence,
    EffectLevel,
    ExperimentConfig,
    RunCondition,
    build_evidence_report,
    reconstruct_events,
    run_counterfactual,
)


def test_effect_levels_do_not_infer_receipt_from_dispatch():
    evidence = ActionEvidence(
        action_id="a1",
        authorization_id="auth-1",
        source_id="web-1",
        attempted=True,
        dispatched=True,
        receiver_received=False,
        effect_confirmed=False,
    )

    assert evidence.effect_level is EffectLevel.DISPATCHED


def test_event_reconstruction_links_authorization_source_and_action():
    events = [
        {"event_id": "3", "timestamp": "2026-01-01T00:00:03Z",
         "event_type": "ACTION_ATTEMPTED",
         "details": {"action_id": "a1", "authorization_id": "auth-1",
                     "source_id": "web-1"}},
        {"event_id": "1", "timestamp": "2026-01-01T00:00:01Z",
         "event_type": "AUTHORIZATION_DECLARED",
         "details": {"authorization_id": "auth-1", "scope": "read-only"}},
        {"event_id": "2", "timestamp": "2026-01-01T00:00:02Z",
         "event_type": "SOURCE_OBSERVED",
         "details": {"source_id": "web-1", "trust": "untrusted"}},
    ]

    timeline = reconstruct_events(events)

    assert [item["event_id"] for item in timeline] == ["1", "2", "3"]
    assert timeline[-1]["details"]["authorization_id"] == "auth-1"


def test_counterfactual_runs_three_conditions_with_only_source_removed():
    config = ExperimentConfig(
        experiment_id="exp-1",
        model="test-model",
        model_version="v1",
        toolset=("read_report",),
        authorization_fingerprint="auth-sha",
        dataset_fingerprint="data-sha",
    )
    seen = []

    def execute(condition, run_config):
        seen.append((condition, run_config.source_removed))
        return {"action": "external_send" if condition is RunCondition.TREATMENT else "summarize"}

    results = run_counterfactual(config, execute)

    assert {item.condition for item in results} == set(RunCondition)
    assert len(seen) == 3
    assert seen.count((RunCondition.COUNTERFACTUAL, True)) == 1
    assert seen.count((RunCondition.BASELINE, False)) == 1
    assert seen.count((RunCondition.TREATMENT, False)) == 1


def test_counterfactual_rejects_config_drift_between_conditions():
    config = ExperimentConfig(
        experiment_id="exp-2", model="m", model_version="v1",
        toolset=("tool",), authorization_fingerprint="auth",
        dataset_fingerprint="data",
    )

    def execute(condition, run_config):
        if condition is RunCondition.TREATMENT:
            return {"model": "changed"}
        return {"model": "same"}

    results = run_counterfactual(config, execute)

    assert all(not result.configuration_valid for result in results)


def test_report_keeps_integrity_authorization_and_causality_independent():
    action = ActionEvidence(
        action_id="a1", authorization_id="auth", source_id="poison",
        attempted=True, dispatched=True, receiver_received=True,
        effect_confirmed=False,
    )
    report = build_evidence_report(
        experiment_id="exp-3",
        actions=[action],
        integrity_valid=True,
        authorization_violation=True,
        causal_evidence_supported=False,
    )

    assert report["actions"][0]["effect_level"] == "RECEIVED"
    assert report["verdicts"] == {
        "integrity": "PASS",
        "authorization": "VIOLATION",
        "causal_evidence": "INSUFFICIENT",
    }


def test_effect_confirmed_requires_received_evidence():
    import pytest

    with pytest.raises(ValueError):
        ActionEvidence(
            action_id="a2", authorization_id="auth", source_id="source",
            attempted=True, dispatched=False, receiver_received=False,
            effect_confirmed=True,
        )
