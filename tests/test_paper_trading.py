from app.schemas.trading import Signal
from app.services.paper_trading import PaperTradingService


def test_paper_trading_service_accepts_clear_order(monkeypatch):
    service = PaperTradingService()

    monkeypatch.setattr(service.client, "get_account", lambda: {"cash": "100000.00", "equity": "100000.00", "trading_blocked": False})
    monkeypatch.setattr(service.client, "get_positions", lambda: [])
    monkeypatch.setattr(service.client, "submit_order", lambda **kwargs: {"status": "accepted", "symbol": kwargs["symbol"], "qty": kwargs["qty"]})

    signal = Signal(symbol="AAPL", direction="buy", confidence=0.9, rationale="Bullish")
    result = service.submit_order_from_signal(signal, 5, 100.0)
    assert result["accepted"] is True
    assert result["symbol"] == "AAPL"


def test_paper_trading_service_rejects_blocked_order(monkeypatch):
    service = PaperTradingService()

    monkeypatch.setattr(service.client, "get_account", lambda: {"cash": "1000.00", "equity": "1000.00", "trading_blocked": True})
    monkeypatch.setattr(service.client, "get_positions", lambda: [])

    signal = Signal(symbol="AAPL", direction="buy", confidence=0.1, rationale="blocked")
    result = service.submit_order_from_signal(signal, 100, 100.0)
    assert result["accepted"] is False
