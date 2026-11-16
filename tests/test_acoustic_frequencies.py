import math
import struct
import wave

import pytest

from siren_trap.telemetry.acoustic_analysis import analyze_wav


def _write_tone(path, frequency, sample_rate=48_000, duration=0.1):
    count = int(sample_rate * duration)
    frames = b"".join(
        struct.pack("<h", int(12_000 * math.sin(2 * math.pi * frequency * i / sample_rate)))
        for i in range(count)
    )
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        output.writeframes(frames)


def test_detects_tone_inside_18_to_20_khz_band(tmp_path):
    wav_path = tmp_path / "19khz.wav"
    _write_tone(wav_path, 19_000)

    result = analyze_wav(wav_path)

    assert result["band_peak_detected"] is True
    assert result["band_peak_hz"] == 19_000
    assert result["sample_rate_hz"] == 48_000


def test_does_not_report_low_frequency_tone_as_band_peak(tmp_path):
    wav_path = tmp_path / "1khz.wav"
    _write_tone(wav_path, 1_000)

    result = analyze_wav(wav_path)

    assert result["band_peak_power"] < 1.0


def test_rejects_sample_rate_that_cannot_represent_full_band(tmp_path):
    wav_path = tmp_path / "low-rate.wav"
    _write_tone(wav_path, 10_000, sample_rate=40_000)

    with pytest.raises(ValueError, match="exceed 40 kHz"):
        analyze_wav(wav_path)


def test_rejects_non_16_bit_pcm(tmp_path):
    wav_path = tmp_path / "unsupported.wav"
    with wave.open(str(wav_path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(1)
        output.setframerate(48_000)
        output.writeframes(b"\x00" * 128)

    with pytest.raises(ValueError, match="16-bit PCM"):
        analyze_wav(wav_path)
