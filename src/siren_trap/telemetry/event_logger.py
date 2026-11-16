"""Minimal append-only JSONL event logger."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


class JsonlEventLogger:
    """Persist structured events without evaluating event content."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def record(self, event_type: str, details: dict[str, Any] | None = None) -> dict:
        if not event_type or not isinstance(event_type, str):
            raise ValueError("event_type must be a non-empty string.")
        event = {
            "event_id": str(uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details or {},
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")
        return event
