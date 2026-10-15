from __future__ import annotations

from app.core.validators import validate_market_bars
from app.schemas.market import MarketBar, MarketSnapshot


class MarketDataService:
    @staticmethod
    def normalize_bars(raw_bars: list[dict]) -> list[MarketBar]:
        normalized: list[MarketBar] = []
        for raw in raw_bars:
            normalized.append(
                MarketBar(
                    symbol=str(raw.get("symbol", "UNKNOWN")),
                    timestamp=str(raw.get("timestamp", "")),
                    open=float(raw.get("open", 0.0)),
                    high=float(raw.get("high", 0.0)),
                    low=float(raw.get("low", 0.0)),
                    close=float(raw.get("close", 0.0)),
                    volume=int(raw.get("volume", 0)),
                )
            )
        return normalized

    @staticmethod
    def validate_snapshot(snapshot: MarketSnapshot) -> tuple[bool, list[str]]:
        return validate_market_bars(snapshot.bars)

    @staticmethod
    def build_snapshot(symbol: str, raw_bars: list[dict]) -> MarketSnapshot:
        bars = MarketDataService.normalize_bars(raw_bars)
        if not bars:
            raise ValueError("No market bars were provided")
        snapshot = MarketSnapshot(symbol=symbol, bars=bars)
        snapshot.start_time = bars[0].timestamp
        snapshot.end_time = bars[-1].timestamp
        return snapshot
