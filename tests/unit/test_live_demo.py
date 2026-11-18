from __future__ import annotations

import json

from benchmarks.run_live_demo import run_experiment


def test_live_demo_writes_independent_evidence_outputs(tmp_path):
    report = run_experiment(tmp_path, emit=lambda _: None)

    assert report["execution_mode"] == "SYNTHETIC_SIMULATION"
    assert report["enforcement_mode"] == "SIMULATED_ADAPTER_NOT_HOST_ISOLATION"
    assert report["external_network_used"] is False
    assert report["verdicts"]["integrity"] == "PASS"
    assert report["verdicts"]["authorization"] == "VIOLATION"
    assert report["verdicts"]["causal_evidence"] == "SUPPORTED"
    assert (tmp_path / "evidence_report.json").is_file()
    assert (tmp_path / "evidence_report.html").is_file()
    assert (tmp_path / "event_timeline.jsonl").is_file()
    events = [json.loads(line) for line in
              (tmp_path / "event_timeline.jsonl").read_text().splitlines()]
    assert "LURE_INTERACTION_CAPTURED" in [event["event_type"] for event in events]
    assert "SENTINEL_CONTAINMENT_RESULT" in [event["event_type"] for event in events]
    action = report["actions"][0]
    assert action["attempted"] is True
    assert action["dispatched"] is False
    assert action["receiver_received"] is False
    assert action["effect_confirmed"] is False


def test_live_demo_documents_simulation_boundary(tmp_path):
    report = run_experiment(tmp_path, emit=lambda _: None)
    assert any("in-memory" in item for item in report["limitations"])
    assert report["receiver_observations"] == []
