"""Bridge the semantic lure layer to Siren's existing fixed ggwave canary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from siren_trap.payload_generator.build_trap import (
    CANARY_MARKER,
    encode_canary,
    write_wav,
)
from siren_trap.telemetry.event_logger import JsonlEventLogger


@dataclass(frozen=True)
class AcousticLureResult:
    """Metadata for a generated fixed acoustic research lure."""

    marker: str
    output_path: str
    sha256: str


def generate_acoustic_lure(
    destination: Path,
    *,
    event_logger: JsonlEventLogger | None = None,
) -> AcousticLureResult:
    """Generate the fixed ggwave marker; arbitrary payloads are not accepted."""
    if not isinstance(destination, Path):
        raise TypeError("destination must be a pathlib.Path.")

    digest = write_wav(encode_canary(), destination)
    if event_logger is not None:
        event_logger.record(
            "ACOUSTIC_LURE_GENERATED",
            {"marker": CANARY_MARKER, "sha256": digest},
        )

    return AcousticLureResult(
        marker=CANARY_MARKER,
        output_path=str(destination),
        sha256=digest,
    )
