from app.strategies.moving_average import MovingAverageStrategy


def test_moving_average_signal_buy():
    strategy = MovingAverageStrategy()
    signal = strategy.generate_signal([100, 101, 102, 103, 104], "AAPL")
    assert signal.direction == "buy"
    assert signal.confidence > 0


def test_moving_average_signal_sell():
    strategy = MovingAverageStrategy()
    signal = strategy.generate_signal([104, 103, 102, 101, 100], "AAPL")
    assert signal.direction == "sell"
    assert signal.confidence > 0


def test_moving_average_signal_hold_when_data_is_insufficient():
    strategy = MovingAverageStrategy()
    signal = strategy.generate_signal([100], "AAPL")
    assert signal.direction == "hold"
