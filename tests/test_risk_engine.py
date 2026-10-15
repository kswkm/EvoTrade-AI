from app.schemas.trading import AccountSnapshot, OrderCandidate
from app.services.risk_engine import RiskEngine


def test_order_allowed_under_limits():
    account = AccountSnapshot(cash=100000.0, equity=100000.0, daily_loss_pct=0.01)
    candidate = OrderCandidate(symbol="AAPL", side="buy", quantity=10, price=100.0)
    decision = RiskEngine(max_position_value=100000.0, max_daily_loss_pct=0.05, max_order_value_pct=0.20).evaluate_order(
        candidate, account
    )

    assert decision.allowed is True
    assert decision.reasons == []


def test_order_blocked_when_emergency_stop_is_active():
    account = AccountSnapshot(cash=100000.0, equity=100000.0, emergency_stop=True)
    candidate = OrderCandidate(symbol="AAPL", side="buy", quantity=10, price=100.0)
    decision = RiskEngine().evaluate_order(candidate, account)

    assert decision.allowed is False
    assert "emergency stop is active" in decision.reasons


def test_order_blocked_when_daily_loss_exceeded():
    account = AccountSnapshot(cash=100000.0, equity=100000.0, daily_loss_pct=0.10)
    candidate = OrderCandidate(symbol="AAPL", side="buy", quantity=10, price=100.0)
    decision = RiskEngine().evaluate_order(candidate, account)

    assert decision.allowed is False
    assert "daily loss threshold exceeded" in decision.reasons
