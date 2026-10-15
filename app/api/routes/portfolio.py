from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.portfolio_state import PortfolioState

router = APIRouter(prefix="/api/v1")


class PortfolioUpdateRequest(BaseModel):
    cash: float = Field(default=100000.0, ge=0)
    equity: float = Field(default=100000.0, ge=0)
    emergency_stop: bool = False
    daily_loss_pct: float = 0.0


@router.get("/portfolio")
def get_portfolio() -> dict[str, object]:
    state = PortfolioState()
    state.update_equity()
    return {
        "cash": state.cash,
        "equity": state.equity,
        "emergency_stop": state.emergency_stop,
        "daily_loss_pct": state.daily_loss_pct,
        "positions": {symbol: {"quantity": pos.quantity, "average_cost": pos.average_cost} for symbol, pos in state.positions.items()},
    }


@router.post("/portfolio/update")
def update_portfolio(payload: PortfolioUpdateRequest) -> dict[str, object]:
    state = PortfolioState(
        cash=payload.cash,
        equity=payload.equity,
        emergency_stop=payload.emergency_stop,
        daily_loss_pct=payload.daily_loss_pct,
    )
    state.update_equity()
    return {
        "cash": state.cash,
        "equity": state.equity,
        "emergency_stop": state.emergency_stop,
        "daily_loss_pct": state.daily_loss_pct,
    }
