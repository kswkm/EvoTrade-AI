from app.services.evolution_analyst import EvolutionAnalyst
from app.schemas.trading import Signal


def test_failure_classification():
    assert EvolutionAnalyst.classify_failure("data source stale") == "DATA_ERROR"
    assert EvolutionAnalyst.classify_failure("signal mismatch") == "SIGNAL_ERROR"


def test_experiment_hypothesis_generation():
    result = EvolutionAnalyst.generate_experiment_hypothesis("TIMING_ERROR", "entry was too early")
    assert result["failure_code"] == "TIMING_ERROR"
    assert "time" in result["hypothesis"].lower()


def test_trade_review_payload():
    signal = Signal(symbol="MSFT", direction="buy", confidence=0.82, rationale="Bullish")
    review = EvolutionAnalyst.build_trade_review(signal, "cost assumptions too optimistic")
    assert review["failure_code"] == "COST_ERROR"
    assert review["symbol"] == "MSFT"
