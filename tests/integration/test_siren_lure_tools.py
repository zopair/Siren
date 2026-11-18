import json

from siren_trap.decoy_firewall.app import create_app
from siren_trap.telemetry.event_logger import JsonlEventLogger


def test_flask_lure_catalog_and_access_are_logged(tmp_path):
    log_path = tmp_path / "events.jsonl"
    app = create_app(
        audio_dir=tmp_path,
        event_logger=JsonlEventLogger(log_path),
    )
    client = app.test_client()

    catalog = client.get("/api/lures?context=financial%20report")
    assert catalog.status_code == 200
    assert any(
        item["id"] == "consolidated-finance-index"
        for item in catalog.json["lures"]
    )

    detail = client.get("/api/lures/consolidated-finance-index")
    assert detail.status_code == 200
    assert "synthetic" in detail.json["content"].lower()

    events = [
        json.loads(line)
        for line in log_path.read_text(encoding="utf-8").splitlines()
    ]
    event_types = [event["event_type"] for event in events]
    assert "SEMANTIC_LURE_LISTED" in event_types
    assert "SEMANTIC_LURE_ACCESSED" in event_types


def test_flask_lure_endpoint_rejects_oversized_context(tmp_path):
    app = create_app(
        audio_dir=tmp_path,
        event_logger=JsonlEventLogger(tmp_path / "events.jsonl"),
    )

    response = app.test_client().get("/api/lures?context=" + "x" * 501)

    assert response.status_code == 400


def test_flask_lure_endpoint_does_not_resolve_arbitrary_paths(tmp_path):
    app = create_app(
        audio_dir=tmp_path,
        event_logger=JsonlEventLogger(tmp_path / "events.jsonl"),
    )

    response = app.test_client().get("/api/lures/..%2F..%2Fetc%2Fpasswd")

    assert response.status_code == 404


def test_mcp_tools_are_read_only_and_return_catalogued_lures(tmp_path):
    from siren_trap.siren_lure.mcp_server import SirenMCPServer

    server = SirenMCPServer(
        event_logger=JsonlEventLogger(tmp_path / "events.jsonl")
    )
    listed = server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    names = [tool["name"] for tool in listed["result"]["tools"]]
    assert names == ["list_siren_lures", "open_siren_lure"]

    opened = server.handle(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "open_siren_lure",
                "arguments": {"lure_id": "consolidated-finance-index"},
            },
        }
    )
    assert "synthetic" in opened["result"]["content"][0]["text"].lower()
