from __future__ import annotations

from app.schemas.trading import AccountSnapshot, Signal
from app.services.alpaca_client import AlpacaClient
from app.services.risk_engine import RiskEngine
from app.services.trade_executor import TradeExecutor


class PaperTradingService:
    def __init__(self, risk_engine: RiskEngine | None = None) -> None:
        self.client = AlpacaClient()
        self.risk_engine = risk_engine or RiskEngine()
        self.executor = TradeExecutor(self.risk_engine)

    def get_account_snapshot(self) -> AccountSnapshot:
        account = self.client.get_account()
        cash = float(account.get("cash", 100000.0))
        equity = float(account.get("equity", cash))
        positions = self.client.get_positions()
        current_positions = {entry.get("symbol", "UNKNOWN"): float(entry.get("market_value", 0.0)) for entry in positions}
        return AccountSnapshot(
            cash=cash,
            equity=equity,
            emergency_stop=bool(account.get("trading_blocked", False)),
            daily_loss_pct=0.0,
            current_positions=current_positions,
        )

    def submit_order_from_signal(self, signal: Signal, quantity: int, price: float, strategy_version: str = "v1") -> dict[str, object]:
        account = self.get_account_snapshot()
        decision = self.executor.evaluate_signal(signal, quantity, price, account)
        if not decision.allowed:
            return {
                "accepted": False,
                "symbol": signal.symbol,
                "reasons": decision.reasons,
                "projected_post_trade_equity": decision.projected_post_trade_equity,
            }

        response = self.client.submit_order(
            symbol=signal.symbol,
            side="buy" if signal.direction == "buy" else "sell",
            qty=quantity,
        )

        return {
            "accepted": True,
            "symbol": signal.symbol,
            "alpaca_response": response,
            "projected_post_trade_equity": decision.projected_post_trade_equity,
        }
