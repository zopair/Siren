"""Generate a harmless, fixed Siren-Trap acoustic canary WAV."""

from __future__ import annotations

import argparse
import hashlib
import wave
from pathlib import Path

CANARY_MARKER = "SIREN-CANARY-TEST-001"
SAMPLE_RATE = 48_000


def encode_canary() -> bytes:
    """Encode the fixed research marker using ggwave.

    The marker is intentionally fixed: arbitrary prompt or command payloads
    are not accepted by this proof-of-concept generator.
    """
    try:
        import ggwave
    except ImportError as exc:
        raise RuntimeError(
            "ggwave is required. Install project dependencies first."
        ) from exc

    encoded = ggwave.encode(CANARY_MARKER, protocolId=1, volume=10)
    if not isinstance(encoded, (bytes, bytearray)) or not encoded:
        raise RuntimeError("ggwave returned an empty or invalid PCM buffer.")
    if len(encoded) % 2:
        raise RuntimeError("Expected 16-bit PCM data from the ggwave binding.")
    return bytes(encoded)


def write_wav(pcm: bytes, destination: Path) -> str:
    """Write mono signed 16-bit PCM to a WAV file and return its SHA-256."""
    if not pcm or len(pcm) % 2:
        raise ValueError("PCM must contain a non-empty sequence of 16-bit samples.")

    destination.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(destination), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(SAMPLE_RATE)
        output.writeframes(pcm)

    return hashlib.sha256(destination.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate the fixed, harmless Siren-Trap acoustic canary."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("assets/audio/canary.wav"),
        help="Destination WAV path.",
    )
    args = parser.parse_args()

    digest = write_wav(encode_canary(), args.output)
    print(f"Canary written: {args.output}")
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()
