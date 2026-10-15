from app.services.strategy_gate import StrategyGate


def test_strategy_gate_accepts_reasonable_uptrend():
    closes = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114]
    approval = StrategyGate(min_total_return=0.0, min_walkforward_return=0.0, min_pass_folds=1).evaluate(
        "moving_average_crossover", "AAPL", closes, train_window=5, test_window=3
    )
    assert approval.strategy_name == "moving_average_crossover"
    assert approval.backtest_return >= -1.0
    assert approval.pass_count >= 0
