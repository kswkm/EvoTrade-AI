from app.services.market_data_service import MarketDataService


def test_market_data_service_normalizes_bars():
    raw = [
        {"symbol": "AAPL", "timestamp": "2024-01-01T00:00:00Z", "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 1000},
        {"symbol": "AAPL", "timestamp": "2024-01-01T00:01:00Z", "open": 100.5, "high": 102.0, "low": 100.0, "close": 101.2, "volume": 1100},
    ]
    snapshot = MarketDataService.build_snapshot("AAPL", raw)
    assert snapshot.symbol == "AAPL"
    assert len(snapshot.bars) == 2
    assert snapshot.start_time == "2024-01-01T00:00:00Z"
