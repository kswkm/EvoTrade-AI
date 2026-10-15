from __future__ import annotations

from app.services.alpaca_client import AlpacaClient
from app.services.backtester import Backtester
from app.services.experiment_manager import ExperimentManager
from app.services.market_data_service import MarketDataService
from app.services.persistence import persist_experiment_result, persist_market_bars, persist_strategy_version, persist_trade_record
from app.services.strategy_gate import StrategyGate
from app.services.walkforward import WalkforwardValidator


class AutomationService:
    def __init__(self) -> None:
        self.client = AlpacaClient()

    def run_cycle(self, symbol: str, closes: list[float] | None = None, strategy_name: str = "moving_average_crossover") -> dict:
        if closes is None:
            raw = self.client.get_market_data(symbol, limit=30)
            normalized = MarketDataService.normalize_bars(raw)
            closes = [bar.close for bar in normalized]

        if len(closes) < 8:
            return {"status": "skipped", "reason": "insufficient closes for automation cycle"}

        backtest = Backtester(initial_cash=100000.0).run(symbol, closes, strategy_name=strategy_name)
        walkforward = WalkforwardValidator(initial_cash=100000.0).validate(symbol, closes, train_window=5, test_window=3)
        gate = StrategyGate()
        approval = gate.evaluate(strategy_name, symbol, closes, train_window=5, test_window=3)

        persist_market_bars(symbol, [{
            "symbol": symbol,
            "timestamp": f"2026-01-01T00:00:{idx:02d}Z",
            "open": price,
            "high": price + 1.0,
            "low": price - 1.0,
            "close": price,
            "volume": 1000 + idx,
        } for idx, price in enumerate(closes)], source="automation")

        persist_strategy_version(
            strategy_name,
            "v1",
            "automated evaluation cycle",
            backtest_return=backtest.total_return,
            walkforward_return=walkforward.average_test_return,
            approved=approval.approved,
        )

        if backtest.trades:
            for trade in backtest.trades[:1]:
                persist_trade_record(symbol, trade.action, trade.quantity, trade.price, "v1", notes=trade.signal)

        experiment = ExperimentManager().run_experiment(
            strategy_name,
            "automated validation cycle",
            approval.backtest_return,
            approval.walkforward_average_return,
        )
        persist_experiment_result(
            strategy_name,
            "automated validation cycle",
            approval.backtest_return,
            approval.walkforward_average_return,
            experiment.winner,
            experiment.status,
        )

        return {
            "status": "ok",
            "symbol": symbol,
            "strategy": strategy_name,
            "approved": approval.approved,
            "backtest_return": round(backtest.total_return, 6),
            "walkforward_average_return": round(walkforward.average_test_return, 6),
            "reasons": approval.reasons,
            "trade_count": backtest.trade_count,
        }
