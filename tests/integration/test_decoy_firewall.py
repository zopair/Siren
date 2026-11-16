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


def test_decoy_page_records_visit_and_exposes_research_scope(tmp_path):
    log_path = tmp_path / "events.jsonl"
    app = create_app(
        audio_dir=tmp_path,
        event_logger=JsonlEventLogger(log_path),
    )
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"Observe the boundary" in response.data
    assert b"Local research node" in response.data
    assert b"Fixed canary" in response.data
    assert b'id="play"' in response.data
    assert b'id="status"' in response.data
    assert b"Authorized environments only" in response.data
    assert b"Copyright \xc2\xa9 2026 ALY HUSSEIN FEKRY ZOPAIR" in response.data
    assert "DECOY_VISIT" in log_path.read_text(encoding="utf-8")


def test_missing_audio_returns_404(tmp_path):
    app = create_app(
        audio_dir=tmp_path / "missing",
        event_logger=JsonlEventLogger(tmp_path / "events.jsonl"),
    )
    response = app.test_client().get("/audio/canary.wav")
    assert response.status_code == 404



def test_decoy_page_exposes_accessible_interactive_architecture(tmp_path):
    app = create_app(
        audio_dir=tmp_path,
        event_logger=JsonlEventLogger(tmp_path / "events.jsonl"),
    )
    response = app.test_client().get("/")
    page = response.data

    assert response.status_code == 200
    assert b'id="architecture-map"' in page
    assert b'data-component="canary"' in page
    assert b'data-component="telemetry"' in page
    assert b'aria-pressed="false"' in page
    assert b'id="architecture-detail"' in page
    assert b"prefers-reduced-motion" in page


def test_readme_embeds_architecture_visual_and_links_local_interactive_preview():
    from pathlib import Path

    repository_root = Path(__file__).resolve().parents[2]
    readme = (repository_root / "README.md").read_text(encoding="utf-8")
    diagram = repository_root / "docs" / "assets" / "siren-trap-architecture.svg"

    assert diagram.is_file()
    assert "docs/assets/siren-trap-architecture.svg" in readme
    assert "interactive architecture" in readme.lower()
    assert "127.0.0.1:5000" in readme
