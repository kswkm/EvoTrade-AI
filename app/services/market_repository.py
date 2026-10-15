from __future__ import annotations

from app.db.models import MarketBarRecord
from app.db.session import SessionLocal
from app.schemas.market import MarketBar


def save_market_bars(symbol: str, bars: list[MarketBar], source: str = "alpaca") -> int:
    try:
        session = SessionLocal()
    except Exception:
        return 0

    try:
        count = 0
        for bar in bars:
            session.merge(
                MarketBarRecord(
                    symbol=bar.symbol or symbol,
                    timestamp=bar.timestamp,
                    open=bar.open,
                    high=bar.high,
                    low=bar.low,
                    close=bar.close,
                    volume=bar.volume,
                    source=source,
                )
            )
            count += 1
        session.commit()
        return count
    except Exception:
        return 0
    finally:
        session.close()
