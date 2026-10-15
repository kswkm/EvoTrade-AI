from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.strategy_gate import StrategyGate

router = APIRouter(prefix="/api/v1")


class StrategyApprovalRequest(BaseModel):
    strategy_name: str = Field(default="moving_average_crossover")
    symbol: str = Field(..., min_length=1, max_length=16)
    closes: list[float] = Field(..., min_length=8)
    train_window: int = Field(default=5, ge=2)
    test_window: int = Field(default=3, ge=1)


@router.post("/strategy/approve")
def evaluate_strategy_approval(payload: StrategyApprovalRequest) -> dict[str, object]:
    gate = StrategyGate()
    approval = gate.evaluate(
        payload.strategy_name,
        payload.symbol,
        payload.closes,
        train_window=payload.train_window,
        test_window=payload.test_window,
    )
    return {
        "strategy_name": approval.strategy_name,
        "approved": approval.approved,
        "reasons": approval.reasons,
        "backtest_return": round(approval.backtest_return, 6),
        "walkforward_average_return": round(approval.walkforward_average_return, 6),
        "pass_count": approval.pass_count,
    }
