import json

from siren_trap.telemetry.event_logger import JsonlEventLogger


def test_records_structured_jsonl_event(tmp_path):
    path = tmp_path / "events" / "events.jsonl"
    event = JsonlEventLogger(path).record("TEST_EVENT", {"safe": True})

    stored = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    assert stored["event_id"] == event["event_id"]
    assert stored["event_type"] == "TEST_EVENT"
    assert stored["details"] == {"safe": True}
    assert stored["timestamp"]
