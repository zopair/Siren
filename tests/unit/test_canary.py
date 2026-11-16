import pytest

from siren_trap.detection.canary import (
    CANARY_MARKER,
    inspect_observation,
)


def test_detects_known_canary_marker():
    result = inspect_observation(f"decoded: {CANARY_MARKER}")
    assert result.detected is True
    assert result.category == "CANARY_OBSERVED"
    assert result.marker == CANARY_MARKER


def test_unrelated_observation_is_not_a_match():
    result = inspect_observation("ordinary environmental description")
    assert result.detected is False
    assert result.category == "NO_MATCH"
    assert result.marker is None


def test_rejects_non_text_observations():
    with pytest.raises(TypeError):
        inspect_observation(None)
