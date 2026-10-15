from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.schemas.trading import AccountSnapshot, OrderCandidate
from app.services.risk_engine import RiskEngine

router = APIRouter(prefix="/api/v1")


class RiskOrderRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    side: str = Field(default="buy")
    quantity: int = Field(default=1, ge=1)
    price: float = Field(default=100.0, gt=0)
    cash: float = Field(default=100000.0, ge=0)
    equity: float = Field(default=100000.0, ge=0)
    emergency_stop: bool = False
    daily_loss_pct: float = 0.0
    current_positions: dict[str, float] = {}


@router.post("/risk/validate-order")
def validate_order(payload: RiskOrderRequest) -> dict[str, object]:
    engine = RiskEngine()
    account = AccountSnapshot(
        cash=payload.cash,
        equity=payload.equity,
        emergency_stop=payload.emergency_stop,
        daily_loss_pct=payload.daily_loss_pct,
        current_positions=payload.current_positions,
    )
    candidate = OrderCandidate(
        symbol=payload.symbol,
        side=payload.side,
        quantity=payload.quantity,
        price=payload.price,
    )
    decision = engine.evaluate_order(candidate, account)
    return {
        "allowed": decision.allowed,
        "reasons": decision.reasons,
        "max_position_value": decision.max_position_value,
        "projected_post_trade_equity": decision.projected_post_trade_equity,
    }
