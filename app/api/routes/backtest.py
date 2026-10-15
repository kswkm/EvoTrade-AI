from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.backtester import Backtester

router = APIRouter(prefix="/api/v1")


class BacktestRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    closes: list[float] = Field(..., min_length=2)
    strategy_name: str = Field(default="moving_average_crossover")
    initial_cash: float = Field(default=100000.0, gt=0)


@router.post("/backtest/run")
def run_backtest(payload: BacktestRequest) -> dict[str, object]:
    backtester = Backtester(initial_cash=payload.initial_cash)
    result = backtester.run(payload.symbol, payload.closes, strategy_name=payload.strategy_name)
    return {
        "symbol": result.symbol,
        "initial_cash": result.initial_cash,
        "final_cash": result.final_cash,
        "final_equity": result.final_equity,
        "total_return": round(result.total_return, 6),
        "sharpe_ratio": round(result.sharpe_ratio, 6),
        "max_drawdown": round(result.max_drawdown, 6),
        "trade_count": len(result.trades),
        "signals": result.signals,
    }
