from __future__ import annotations

from app.schemas.market import MarketBar


def validate_market_bars(bars: list[MarketBar]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not bars:
        return False, ["market data is empty"]

    for index, bar in enumerate(bars):
        if bar.high < bar.low:
            reasons.append(f"bar {index} has high < low")
        if bar.open <= 0 or bar.close <= 0:
            reasons.append(f"bar {index} has non-positive price")
        if bar.volume < 0:
            reasons.append(f"bar {index} has negative volume")

    return not reasons, reasons
