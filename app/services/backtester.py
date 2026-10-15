from __future__ import annotations

import math

from app.schemas.backtest import BacktestResult, BacktestTrade
from app.schemas.trading import Signal
from app.strategies.moving_average import MovingAverageStrategy


class Backtester:
    def __init__(self, initial_cash: float = 100000.0) -> None:
        self.initial_cash = float(initial_cash)

    def run(self, symbol: str, closes: list[float], strategy_name: str = "moving_average_crossover") -> BacktestResult:
        if len(closes) < 2:
            raise ValueError("At least two closing prices are required")

        strategy = self._resolve_strategy(strategy_name)
        cash = self.initial_cash
        position = 0
        trades: list[BacktestTrade] = []
        signals: list[str] = []
        equity_curve: list[float] = [self.initial_cash]

        for index in range(1, len(closes)):
            historical = closes[: index + 1]
            signal = strategy.generate_signal(historical, symbol)
            signals.append(signal.direction)
            price = closes[index]

            if signal.direction == "buy" and position <= 0:
                quantity = max(1, int(cash / price))
                if quantity <= 0:
                    continue
                cash -= quantity * price
                position = quantity
                trades.append(
                    BacktestTrade(
                        index=index,
                        price=price,
                        signal=signal.direction,
                        action="buy",
                        quantity=quantity,
                        cash_after=cash,
                        equity_after=cash + position * price,
                    )
                )
            elif signal.direction == "sell" and position > 0:
                cash += position * price
                trades.append(
                    BacktestTrade(
                        index=index,
                        price=price,
                        signal=signal.direction,
                        action="sell",
                        quantity=position,
                        cash_after=cash,
                        equity_after=cash + position * price,
                    )
                )
                position = 0

            equity_value = cash + position * price
            equity_curve.append(equity_value)

        final_cash = cash
        final_equity = cash + position * closes[-1]
        total_return = ((final_equity - self.initial_cash) / self.initial_cash) if self.initial_cash else 0.0

        daily_returns: list[float] = []
        for previous, current in zip(equity_curve[:-1], equity_curve[1:]):
            if previous <= 0:
                continue
            daily_returns.append((current / previous) - 1.0)

        sharpe_ratio = 0.0
        if daily_returns:
            mean_return = sum(daily_returns) / len(daily_returns)
            variance = sum((value - mean_return) ** 2 for value in daily_returns) / len(daily_returns)
            std_dev = math.sqrt(variance)
            sharpe_ratio = (mean_return / std_dev) * math.sqrt(252) if std_dev > 0 else 0.0

        peak = max(equity_curve)
        drawdown = 0.0
        for equity in equity_curve:
            if peak == 0:
                continue
            drawdown = max(drawdown, (peak - equity) / peak)

        return BacktestResult(
            symbol=symbol,
            initial_cash=self.initial_cash,
            final_cash=final_cash,
            final_equity=final_equity,
            total_return=total_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=drawdown,
            trades=trades,
            signals=signals,
        )

    def _resolve_strategy(self, strategy_name: str):
        if strategy_name == "moving_average_crossover":
            return MovingAverageStrategy()
        if strategy_name == "moving_average":
            return MovingAverageStrategy()
        raise ValueError(f"Unsupported strategy: {strategy_name}")
