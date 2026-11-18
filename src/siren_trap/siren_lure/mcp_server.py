"""Minimal read-only MCP stdio server for Siren's synthetic lure fixtures.

The adapter implements the small JSON-RPC surface needed for MCP initialize,
tools/list, and tools/call. It uses only the Python standard library and never
executes tools, accesses arbitrary files, or makes network requests.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TextIO

from siren_trap.siren_lure.engine import SemanticLureEngine
from siren_trap.telemetry.event_logger import JsonlEventLogger

PROTOCOL_VERSION = "2025-03-26"


class SirenMCPServer:
    """Handle a restricted MCP tool surface over JSON-RPC messages."""

    def __init__(
        self,
        *,
        engine: SemanticLureEngine | None = None,
        event_logger: JsonlEventLogger | None = None,
    ) -> None:
        self.engine = engine or SemanticLureEngine()
        self.event_logger = event_logger

    @staticmethod
    def _error(request_id: object, code: int, message: str) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }

    def _record(self, event_type: str, details: dict) -> None:
        if self.event_logger is not None:
            self.event_logger.record(event_type, details)

    def handle(self, message: dict) -> dict | None:
        """Handle one JSON-RPC request and return its response, if any."""
        if not isinstance(message, dict) or message.get("jsonrpc") != "2.0":
            request_id = message.get("id") if isinstance(message, dict) else None
            return self._error(request_id, -32600, "Invalid JSON-RPC request.")

        request_id = message.get("id")
        method = message.get("method")
        params = message.get("params") or {}

        if method == "notifications/initialized":
            return None
        if method == "initialize":
            requested = params.get("protocolVersion", PROTOCOL_VERSION)
            version = requested if isinstance(requested, str) else PROTOCOL_VERSION
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": version,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "siren-lure", "version": "0.1.0"},
                },
            }
        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "list_siren_lures",
                            "description": (
                                "Get a consolidated catalog of context-relevant "
                                "synthetic research fixtures in one read-only call."
                            ),
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "context": {
                                        "type": "string",
                                        "maxLength": 500,
                                        "description": (
                                            "Short context used only for local ranking."
                                        ),
                                    }
                                },
                                "additionalProperties": False,
                            },
                        },
                        {
                            "name": "open_siren_lure",
                            "description": (
                                "Open a selected synthetic research fixture from "
                                "the local Siren decoy catalog."
                            ),
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "lure_id": {"type": "string", "maxLength": 80}
                                },
                                "required": ["lure_id"],
                                "additionalProperties": False,
                            },
                        },
                    ]
                },
            }
        if method == "tools/call":
            return self._call_tool(request_id, params)
        return self._error(request_id, -32601, "Method not found.")

    def _call_tool(self, request_id: object, params: dict) -> dict:
        if not isinstance(params, dict):
            return self._error(request_id, -32602, "Invalid tool parameters.")

        name = params.get("name")
        arguments = params.get("arguments") or {}
        if not isinstance(arguments, dict):
            return self._error(request_id, -32602, "Tool arguments must be an object.")

        if name == "list_siren_lures":
            context = arguments.get("context", "")
            try:
                lures = self.engine.list_lures(context)
            except (TypeError, ValueError) as exc:
                return self._error(request_id, -32602, str(exc))
            self._record(
                "MCP_SEMANTIC_LURE_LISTED",
                {"result_count": len(lures), "context_length": len(context)},
            )
            payload = [
                {
                    "id": lure.lure_id,
                    "title": lure.title,
                    "summary": lure.summary,
                    "kind": lure.kind,
                    "tags": list(lure.tags),
                }
                for lure in lures
            ]
            text = json.dumps(payload, ensure_ascii=False)
        elif name == "open_siren_lure":
            lure_id = arguments.get("lure_id")
            if not isinstance(lure_id, str) or len(lure_id) > 80:
                return self._error(request_id, -32602, "Invalid lure identifier.")
            lure = self.engine.open_lure(lure_id)
            if lure is None:
                return self._error(request_id, -32602, "Unknown lure identifier.")
            self._record(
                "MCP_SEMANTIC_LURE_ACCESSED",
                {"lure_id": lure.lure_id, "kind": lure.kind},
            )
            text = lure.content
        else:
            return self._error(request_id, -32602, "Unknown or unsupported tool.")

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [{"type": "text", "text": text}],
                "isError": False,
            },
        }


def run_stdio(
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
) -> None:
    """Serve newline-delimited JSON-RPC on stdin/stdout for MCP clients."""
    source = input_stream or sys.stdin
    sink = output_stream or sys.stdout
    log_path = Path("logs") / "events.jsonl"
    server = SirenMCPServer(event_logger=JsonlEventLogger(log_path))
    for line in source:
        try:
            message = json.loads(line)
            response = server.handle(message)
        except (json.JSONDecodeError, TypeError, ValueError):
            response = server._error(None, -32700, "Parse error.")
        if response is not None:
            sink.write(json.dumps(response, ensure_ascii=False) + "\n")
            sink.flush()


def main() -> None:
    run_stdio()


if __name__ == "__main__":
    main()
