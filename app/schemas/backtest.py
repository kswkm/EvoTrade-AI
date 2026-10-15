from dataclasses import dataclass, field


@dataclass
class BacktestTrade:
    index: int
    price: float
    signal: str
    action: str
    quantity: int
    cash_after: float
    equity_after: float


@dataclass
class BacktestResult:
    symbol: str
    initial_cash: float
    final_cash: float
    final_equity: float
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    trades: list[BacktestTrade] = field(default_factory=list)
    signals: list[str] = field(default_factory=list)

    @property
    def trade_count(self) -> int:
        return len(self.trades)
