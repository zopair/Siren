"""Local, instrumented decoy service for authorized research."""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, send_from_directory

from siren_trap.siren_lure.engine import SemanticLureEngine
from siren_trap.siren_lure.flask_tools import create_lure_blueprint
from siren_trap.telemetry.event_logger import JsonlEventLogger

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
AUDIO_DIR = REPOSITORY_ROOT / "assets" / "audio"


def create_app(
    *,
    audio_dir: Path | None = None,
    event_logger: JsonlEventLogger | None = None,
    lure_engine: SemanticLureEngine | None = None,
) -> Flask:
    """Create the Flask app with injectable paths for deterministic tests."""
    app = Flask(__name__, template_folder="templates")
    selected_audio_dir = audio_dir or AUDIO_DIR
    logger = event_logger or JsonlEventLogger(
        Path(os.getenv("SIREN_LOG_DIR", "logs")) / "events.jsonl"
    )
    app.register_blueprint(
        create_lure_blueprint(engine=lure_engine, event_logger=logger)
    )

    @app.after_request
    def apply_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; media-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self' 'unsafe-inline'; "
            "object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
        )
        return response

    @app.get("/")
    def index():
        logger.record("DECOY_VISIT", {"request_id": str(uuid.uuid4())})
        return render_template("decoy.html")

    @app.get("/audio/canary.wav")
    def canary_audio():
        path = selected_audio_dir / "canary.wav"
        if not path.is_file():
            return jsonify(
                {"status": "unavailable", "message": "Canary not generated."}
            ), 404

        logger.record("CANARY_AUDIO_REQUEST", {"request_id": str(uuid.uuid4())})
        return send_from_directory(
            selected_audio_dir,
            "canary.wav",
            mimetype="audio/wav",
            as_attachment=True,
            download_name="siren-canary.wav",
        )

    @app.get("/health")
    def health():
        return jsonify(
            {
                "service": "Siren-Trap",
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.getenv("SIREN_HOST", "127.0.0.1"),
        port=int(os.getenv("SIREN_PORT", "5000")),
        debug=False,
    )
