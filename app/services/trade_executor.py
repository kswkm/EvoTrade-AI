from __future__ import annotations

from app.schemas.trading import AccountSnapshot, OrderCandidate, RiskDecision, Signal
from app.services.risk_engine import RiskEngine


class TradeExecutor:
    def __init__(self, risk_engine: RiskEngine | None = None) -> None:
        self.risk_engine = risk_engine or RiskEngine()

    def build_order_candidate(self, signal: Signal, quantity: int, price: float, strategy_version: str = "v1") -> OrderCandidate:
        side = signal.direction
        if side == "hold":
            side = "hold"
        elif side == "sell":
            side = "sell"
        else:
            side = "buy"

        return OrderCandidate(
            symbol=signal.symbol,
            side=side,
            quantity=quantity,
            price=price,
            strategy_version=strategy_version,
            notes=signal.rationale,
        )

    def evaluate_signal(self, signal: Signal, quantity: int, price: float, account: AccountSnapshot) -> RiskDecision:
        candidate = self.build_order_candidate(signal, quantity, price)
        return self.risk_engine.evaluate_order(candidate, account)
