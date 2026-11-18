import pytest

from siren_trap.siren_lure.acoustic import generate_acoustic_lure


def test_acoustic_lure_wraps_existing_fixed_ggwave_generator(tmp_path, monkeypatch):
    import siren_trap.siren_lure.acoustic as acoustic

    monkeypatch.setattr(acoustic, "encode_canary", lambda: b"\x00\x00")
    monkeypatch.setattr(acoustic, "write_wav", lambda pcm, path: "a" * 64)

    result = generate_acoustic_lure(tmp_path / "canary.wav")

    assert result.marker == "SIREN-CANARY-TEST-001"
    assert result.sha256 == "a" * 64
    assert result.output_path == str(tmp_path / "canary.wav")


def test_acoustic_lure_requires_path_object():
    with pytest.raises(TypeError):
        generate_acoustic_lure("canary.wav")
