from app.services.walkforward import WalkforwardValidator


def test_walkforward_validator_returns_fold_summary():
    closes = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114]
    result = WalkforwardValidator(initial_cash=100000.0).validate("AAPL", closes, train_window=5, test_window=3)
    assert result.symbol == "AAPL"
    assert len(result.folds) >= 1
    assert result.pass_count >= 0
    assert result.average_test_return >= -1.0
