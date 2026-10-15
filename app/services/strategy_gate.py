from __future__ import annotations

from dataclasses import dataclass, field

from app.services.backtester import Backtester
from app.services.walkforward import WalkforwardValidator


@dataclass
class StrategyApproval:
    strategy_name: str
    approved: bool
    reasons: list[str] = field(default_factory=list)
    backtest_return: float = 0.0
    walkforward_average_return: float = 0.0
    pass_count: int = 0


class StrategyGate:
    def __init__(
        self,
        min_total_return: float = 0.0,
        min_walkforward_return: float = 0.0,
        min_pass_folds: int = 1,
        max_drawdown: float = 0.40,
    ) -> None:
        self.min_total_return = min_total_return
        self.min_walkforward_return = min_walkforward_return
        self.min_pass_folds = min_pass_folds
        self.max_drawdown = max_drawdown

    def evaluate(self, strategy_name: str, symbol: str, closes: list[float], train_window: int = 5, test_window: int = 3) -> StrategyApproval:
        if len(closes) < 8:
            raise ValueError("Not enough data to evaluate strategy approval")

        backtest = Backtester(initial_cash=100000.0).run(symbol, closes, strategy_name=strategy_name)
        walkforward = WalkforwardValidator(initial_cash=100000.0, min_pass_folds=self.min_pass_folds).validate(
            symbol, closes, train_window=train_window, test_window=test_window
        )

        reasons: list[str] = []
        if backtest.total_return < self.min_total_return:
            reasons.append("total return below minimum threshold")
        if walkforward.average_test_return < self.min_walkforward_return:
            reasons.append("walk-forward average return below minimum threshold")
        if walkforward.pass_count < self.min_pass_folds:
            reasons.append("insufficient positive walk-forward folds")
        if backtest.max_drawdown > self.max_drawdown:
            reasons.append("max drawdown exceeds allowable threshold")

        approved = len(reasons) == 0
        return StrategyApproval(
            strategy_name=strategy_name,
            approved=approved,
            reasons=reasons,
            backtest_return=backtest.total_return,
            walkforward_average_return=walkforward.average_test_return,
            pass_count=walkforward.pass_count,
        )
