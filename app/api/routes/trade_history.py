from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.trade_history import TradeHistory

router = APIRouter(prefix="/api/v1")

history = TradeHistory()


class TradeHistoryRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    side: str = Field(default="buy")
    quantity: int = Field(default=1, ge=1)
    price: float = Field(default=100.0, gt=0)
    strategy_version: str = Field(default="v1")
    notes: str = ""


@router.get("/trades")
def list_trades() -> dict[str, list[dict[str, object]]]:
    return {"trades": [
        {
            "symbol": r.symbol,
            "side": r.side,
            "quantity": r.quantity,
            "price": r.price,
            "strategy_version": r.strategy_version,
            "timestamp": r.timestamp,
            "notes": r.notes,
        }
        for r in history.list_records()
    ]}


@router.post("/trades/record")
def record_trade(payload: TradeHistoryRequest) -> dict[str, object]:
    record = history.add_record(
        payload.symbol,
        payload.side,
        payload.quantity,
        payload.price,
        payload.strategy_version,
        notes=payload.notes,
    )
    return {
        "symbol": record.symbol,
        "side": record.side,
        "quantity": record.quantity,
        "price": record.price,
        "strategy_version": record.strategy_version,
        "timestamp": record.timestamp,
    }
