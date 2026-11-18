import pytest

from siren_trap.siren_lure.engine import SemanticLureEngine


def test_catalog_contains_only_fixed_synthetic_lure_assets():
    engine = SemanticLureEngine()

    lures = engine.list_lures("financial report")

    assert lures
    assert any(lure.lure_id == "consolidated-finance-index" for lure in lures)
    assert all("synthetic" in lure.content.lower() for lure in lures)


def test_context_relevance_ranks_matching_lure_first():
    engine = SemanticLureEngine()

    lures = engine.list_lures("financial report quarterly revenue")

    assert lures[0].lure_id == "consolidated-finance-index"


def test_open_lure_returns_only_catalogued_resources():
    engine = SemanticLureEngine()

    assert engine.open_lure("../secrets") is None
    assert engine.open_lure("consolidated-finance-index") is not None


def test_context_must_be_bounded_text():
    engine = SemanticLureEngine()

    with pytest.raises(TypeError):
        engine.list_lures(None)
    with pytest.raises(ValueError):
        engine.list_lures("x" * 501)
