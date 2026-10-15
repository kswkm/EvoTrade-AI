from __future__ import annotations

from dataclasses import dataclass, field

from app.services.backtester import Backtester


@dataclass
class WalkforwardFold:
    train_start: int
    train_end: int
    test_start: int
    test_end: int
    train_return: float
    test_return: float
    pass_threshold: bool


@dataclass
class WalkforwardResult:
    symbol: str
    folds: list[WalkforwardFold] = field(default_factory=list)
    average_test_return: float = 0.0
    pass_count: int = 0


class WalkforwardValidator:
    def __init__(self, initial_cash: float = 100000.0, min_pass_folds: int = 1) -> None:
        self.initial_cash = initial_cash
        self.min_pass_folds = min_pass_folds

    def validate(self, symbol: str, closes: list[float], train_window: int = 5, test_window: int = 3) -> WalkforwardResult:
        if len(closes) < train_window + test_window:
            raise ValueError("Not enough data for walk-forward validation")

        folds: list[WalkforwardFold] = []
        for start in range(0, len(closes) - train_window - test_window + 1, test_window):
            train_slice = closes[start:start + train_window]
            test_slice = closes[start + train_window:start + train_window + test_window]
            train_result = Backtester(initial_cash=self.initial_cash).run(symbol, train_slice)
            test_result = Backtester(initial_cash=self.initial_cash).run(symbol, test_slice)

            fold = WalkforwardFold(
                train_start=start,
                train_end=start + train_window - 1,
                test_start=start + train_window,
                test_end=start + train_window + test_window - 1,
                train_return=train_result.total_return,
                test_return=test_result.total_return,
                pass_threshold=(test_result.total_return >= 0.0),
            )
            folds.append(fold)

        avg_return = sum(f.test_return for f in folds) / len(folds) if folds else 0.0
        accepted = sum(1 for f in folds if f.pass_threshold)
        return WalkforwardResult(
            symbol=symbol,
            folds=folds,
            average_test_return=avg_return,
            pass_count=accepted,
        )
