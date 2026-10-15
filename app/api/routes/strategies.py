from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.strategies.moving_average import MovingAverageStrategy

router = APIRouter(prefix="/api/v1")


class StrategySignalRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    close_prices: list[float] = Field(..., min_length=2)


@router.get("/strategies")
def list_strategies() -> dict[str, list[str]]:
    return {"strategies": ["moving_average_crossover"]}


@router.post("/strategies/generate-signal")
def generate_signal(payload: StrategySignalRequest) -> dict[str, object]:
    strategy = MovingAverageStrategy()
    signal = strategy.generate_signal(payload.close_prices, payload.symbol)
    return {
        "symbol": signal.symbol,
        "direction": signal.direction,
        "confidence": round(signal.confidence, 4),
        "rationale": signal.rationale,
    }
