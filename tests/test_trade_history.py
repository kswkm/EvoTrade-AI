from app.services.trade_history import TradeHistory


def test_trade_history_records_trades():
    history = TradeHistory()
    record = history.add_record("AAPL", "buy", 10, 100.0, "v1", notes="initial buy")
    assert record.symbol == "AAPL"
    assert record.side == "buy"
    assert len(history.list_records()) == 1
