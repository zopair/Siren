"""Small, dependency-free spectral checks for recorded WAV files.

This is passive analysis only: it does not play, transmit, or decode audio.
"""
from __future__ import annotations

import argparse
import json
import math
import wave
from pathlib import Path
from typing import Any

BAND_LOW_HZ = 18_000
BAND_HIGH_HZ = 20_000
SCAN_STEP_HZ = 100
MAX_ANALYSIS_SECONDS = 0.5


def _goertzel_power(samples: list[float], sample_rate: int, frequency: int) -> float:
    omega = 2.0 * math.pi * frequency / sample_rate
    coefficient = 2.0 * math.cos(omega)
    previous = 0.0
    previous_previous = 0.0
    for sample in samples:
        current = sample + coefficient * previous - previous_previous
        previous_previous, previous = previous, current
    return max(
        0.0,
        previous * previous
        + previous_previous * previous_previous
        - coefficient * previous * previous_previous,
    )


def analyze_wav(path: Path) -> dict[str, Any]:
    """Measure peak Goertzel power from 18–20 kHz in a WAV recording."""
    with wave.open(str(path), "rb") as audio:
        channels = audio.getnchannels()
        width = audio.getsampwidth()
        sample_rate = audio.getframerate()
        frame_count = audio.getnframes()
        if width != 2:
            raise ValueError("Only 16-bit PCM WAV files are supported.")
        if sample_rate <= 2 * BAND_HIGH_HZ:
            raise ValueError(
                "Sample rate must exceed 40 kHz to analyze the full 18–20 kHz band."
            )
        if frame_count == 0:
            raise ValueError("WAV file contains no audio frames.")
        frames_to_read = min(frame_count, int(sample_rate * MAX_ANALYSIS_SECONDS))
        raw = audio.readframes(frames_to_read)

    import array

    values = array.array("h")
    values.frombytes(raw)
    if values.itemsize != 2:
        raise RuntimeError("This platform does not provide 16-bit signed samples.")
    if __import__("sys").byteorder != "little":
        values.byteswap()

    mono: list[float] = []
    for offset in range(0, len(values), channels):
        mono.append(sum(values[offset : offset + channels]) / channels / 32768.0)
    if not mono:
        raise ValueError("WAV file contains no decodable samples.")

    frequencies = range(BAND_LOW_HZ, BAND_HIGH_HZ + 1, SCAN_STEP_HZ)
    measurements = {
        frequency: _goertzel_power(mono, sample_rate, frequency)
        for frequency in frequencies
    }
    peak_frequency = max(measurements, key=measurements.get)
    peak_power = measurements[peak_frequency]
    total_power = sum(sample * sample for sample in mono)

    return {
        "sample_rate_hz": sample_rate,
        "channels": channels,
        "analyzed_seconds": len(mono) / sample_rate,
        "band_hz": [BAND_LOW_HZ, BAND_HIGH_HZ],
        "band_peak_hz": peak_frequency,
        "band_peak_power": peak_power,
        "band_peak_detected": peak_power > 0.0,
        "sample_rms": math.sqrt(total_power / len(mono)),
        "analysis_note": (
            "A spectral peak is not proof of inaudibility, microphone pickup, "
            "or successful decoding."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Passively inspect 18–20 kHz energy in a 16-bit PCM WAV file."
    )
    parser.add_argument("wav_file", type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze_wav(args.wav_file), indent=2))


if __name__ == "__main__":
    main()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Passively inspect 18–20 kHz energy in a 16-bit PCM WAV file."
    )
    parser.add_argument("wav_file", type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze_wav(args.wav_file), indent=2))


if __name__ == "__main__":
    main()
