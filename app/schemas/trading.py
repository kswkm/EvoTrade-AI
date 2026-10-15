from dataclasses import dataclass, field
from typing import Literal


@dataclass
class OrderCandidate:
    symbol: str
    side: Literal["buy", "sell", "hold"]
    quantity: int
    price: float
    strategy_version: str = "v1"
    notes: str = ""

    @property
    def order_value(self) -> float:
        return self.quantity * self.price


@dataclass
class AccountSnapshot:
    cash: float = 0.0
    equity: float = 0.0
    emergency_stop: bool = False
    daily_loss_pct: float = 0.0
    current_positions: dict[str, float] = field(default_factory=dict)


@dataclass
class RiskDecision:
    allowed: bool
    reasons: list[str] = field(default_factory=list)
    max_position_value: float | None = None
    projected_post_trade_equity: float | None = None


@dataclass
class Signal:
    symbol: str
    direction: Literal["buy", "sell", "hold"]
    confidence: float
    rationale: str
