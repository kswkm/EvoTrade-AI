from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.validators import validate_market_bars
from app.schemas.market import MarketBar
from app.services.alpaca_client import AlpacaClient
from app.services.market_data_service import MarketDataService
from app.services.market_repository import save_market_bars
from app.strategies.moving_average import MovingAverageStrategy

router = APIRouter(prefix="/api/v1")


class SignalRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    close_prices: list[float] = Field(..., min_length=2)


class HistoricalMarketRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    limit: int = Field(default=30, ge=2, le=1000)
    timeframe: str = Field(default="1Day")


@router.post("/market/signal")
def produce_signal(payload: SignalRequest) -> dict[str, object]:
    strategy = MovingAverageStrategy()
    signal = strategy.generate_signal(payload.close_prices, payload.symbol)
    return {
        "symbol": signal.symbol,
        "direction": signal.direction,
        "confidence": round(signal.confidence, 4),
        "rationale": signal.rationale,
    }


@router.post("/market/historical")
def fetch_historical_market_data(payload: HistoricalMarketRequest) -> dict[str, object]:
    client = AlpacaClient()
    raw_bars = client.get_market_data(payload.symbol, limit=payload.limit, timeframe=payload.timeframe)
    bars = MarketDataService.normalize_bars(raw_bars)
    valid, reasons = validate_market_bars(bars)
    if not valid:
        return {"symbol": payload.symbol, "valid": False, "reasons": reasons, "bars": []}
    try:
        save_market_bars(payload.symbol, bars, source="alpaca")
    except Exception:
        pass
    return {"symbol": payload.symbol, "valid": True, "count": len(bars), "bars": [bar.model_dump() for bar in bars]}


@router.post("/market/validate")
def validate_market(payload: HistoricalMarketRequest) -> dict[str, object]:
    client = AlpacaClient()
    raw_bars = client.get_market_data(payload.symbol, limit=payload.limit, timeframe=payload.timeframe)
    bars = MarketDataService.normalize_bars(raw_bars)
    valid, reasons = validate_market_bars(bars)
    return {"symbol": payload.symbol, "valid": valid, "reasons": reasons, "count": len(bars)}
