from app.services.backtester import Backtester


def test_backtester_generates_results_for_uptrend():
    closes = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    result = Backtester(initial_cash=100000.0).run("AAPL", closes)
    assert result.symbol == "AAPL"
    assert result.final_equity > 0
    assert result.trade_count >= 0
    assert len(result.signals) == len(closes) - 1


def test_backtester_rejects_too_short_series():
    try:
        Backtester().run("AAPL", [100])
        assert False, "Expected ValueError"
    except ValueError:
        pass
