from pydantic import BaseModel, Field


class MarketBar(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: int = 0


class MarketSnapshot(BaseModel):
    symbol: str
    bars: list[MarketBar]
    start_time: str | None = None
    end_time: str | None = None
