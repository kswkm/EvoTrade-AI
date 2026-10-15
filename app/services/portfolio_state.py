from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PortfolioPosition:
    symbol: str
    quantity: int
    average_cost: float
    market_value: float = 0.0


@dataclass
class PortfolioState:
    cash: float = 100000.0
    equity: float = 100000.0
    emergency_stop: bool = False
    daily_loss_pct: float = 0.0
    positions: dict[str, PortfolioPosition] = field(default_factory=dict)

    def add_position(self, symbol: str, quantity: int, price: float) -> None:
        existing = self.positions.get(symbol)
        if existing is None:
            self.positions[symbol] = PortfolioPosition(symbol=symbol, quantity=quantity, average_cost=price, market_value=quantity * price)
            self.cash -= quantity * price
            return

        total_quantity = existing.quantity + quantity
        total_cost = (existing.quantity * existing.average_cost) + (quantity * price)
        self.positions[symbol] = PortfolioPosition(
            symbol=symbol,
            quantity=total_quantity,
            average_cost=total_cost / total_quantity,
            market_value=total_quantity * price,
        )
        self.cash -= quantity * price

    def liquidate_position(self, symbol: str, price: float) -> None:
        existing = self.positions.get(symbol)
        if existing is None:
            return
        self.cash += existing.quantity * price
        self.positions.pop(symbol, None)

    def update_equity(self) -> None:
        position_value = sum(position.market_value for position in self.positions.values())
        self.equity = self.cash + position_value

    def set_emergency_stop(self, active: bool) -> None:
        self.emergency_stop = active
