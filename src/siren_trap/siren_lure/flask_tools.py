"""Read-only Flask routes exposing the fixed semantic lure catalog."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from siren_trap.siren_lure.engine import SemanticLureEngine
from siren_trap.telemetry.event_logger import JsonlEventLogger


def create_lure_blueprint(
    *,
    engine: SemanticLureEngine | None = None,
    event_logger: JsonlEventLogger,
) -> Blueprint:
    """Create read-only lure routes; all resources come from the fixed catalog."""
    selected_engine = engine or SemanticLureEngine()
    blueprint = Blueprint("siren_lure", __name__, url_prefix="/api/lures")

    @blueprint.get("")
    def list_lures():
        context = request.args.get("context", "")
        try:
            lures = selected_engine.list_lures(context)
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

        event_logger.record(
            "SEMANTIC_LURE_LISTED",
            {"result_count": len(lures), "context_length": len(context)},
        )
        return jsonify({"lures": [
            {
                "id": lure.lure_id,
                "title": lure.title,
                "summary": lure.summary,
                "kind": lure.kind,
                "tags": list(lure.tags),
            }
            for lure in lures
        ]})

    @blueprint.get("/<lure_id>")
    def open_lure(lure_id: str):
        lure = selected_engine.open_lure(lure_id)
        if lure is None:
            return jsonify({"error": "Lure not found."}), 404

        event_logger.record(
            "SEMANTIC_LURE_ACCESSED",
            {"lure_id": lure.lure_id, "kind": lure.kind},
        )
        return jsonify(lure.to_dict())

    return blueprint
