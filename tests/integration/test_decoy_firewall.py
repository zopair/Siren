from siren_trap.decoy_firewall.app import create_app
from siren_trap.telemetry.event_logger import JsonlEventLogger


def test_health_endpoint_and_security_headers(tmp_path):
    app = create_app(
        audio_dir=tmp_path,
        event_logger=JsonlEventLogger(tmp_path / "events.jsonl"),
    )
    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_decoy_page_records_visit(tmp_path):
    log_path = tmp_path / "events.jsonl"
    app = create_app(
        audio_dir=tmp_path,
        event_logger=JsonlEventLogger(log_path),
    )
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"SIREN RESEARCH NODE" in response.data
    assert "DECOY_VISIT" in log_path.read_text(encoding="utf-8")


def test_missing_audio_returns_404(tmp_path):
    app = create_app(
        audio_dir=tmp_path / "missing",
        event_logger=JsonlEventLogger(tmp_path / "events.jsonl"),
    )
    response = app.test_client().get("/audio/canary.wav")
    assert response.status_code == 404
