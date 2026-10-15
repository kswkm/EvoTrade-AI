from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.schemas.trading import AccountSnapshot, Signal
from app.services.trade_executor import TradeExecutor

router = APIRouter(prefix="/api/v1")


class SubmitOrderRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    direction: str = Field(default="buy")
    quantity: int = Field(default=1, ge=1)
    price: float = Field(default=100.0, gt=0)
    cash: float = Field(default=100000.0, ge=0)
    equity: float = Field(default=100000.0, ge=0)
    daily_loss_pct: float = 0.0
    emergency_stop: bool = False
    current_positions: dict[str, float] = {}


@router.post("/orders/validate")
def validate_order(payload: SubmitOrderRequest) -> dict[str, object]:
    signal = Signal(
        symbol=payload.symbol,
        direction=payload.direction,
        confidence=0.8,
        rationale="Simulated order validation",
    )
    account = AccountSnapshot(
        cash=payload.cash,
        equity=payload.equity,
        daily_loss_pct=payload.daily_loss_pct,
        emergency_stop=payload.emergency_stop,
        current_positions=payload.current_positions,
    )
    decision = TradeExecutor().evaluate_signal(signal, payload.quantity, payload.price, account)
    return {
        "allowed": decision.allowed,
        "reasons": decision.reasons,
        "projected_post_trade_equity": decision.projected_post_trade_equity,
    }


@router.post("/orders/submit")
def submit_order(payload: SubmitOrderRequest) -> dict[str, object]:
    signal = Signal(
        symbol=payload.symbol,
        direction=payload.direction,
        confidence=0.8,
        rationale="Order accepted after risk validation",
    )
    account = AccountSnapshot(
        cash=payload.cash,
        equity=payload.equity,
        daily_loss_pct=payload.daily_loss_pct,
        emergency_stop=payload.emergency_stop,
        current_positions=payload.current_positions,
    )
    decision = TradeExecutor().evaluate_signal(signal, payload.quantity, payload.price, account)
    return {
        "accepted": decision.allowed,
        "message": "Order submitted to paper trading system" if decision.allowed else "Order rejected by risk engine",
        "reasons": decision.reasons,
        "symbol": payload.symbol,
    }
