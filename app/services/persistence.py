from __future__ import annotations

from app.db.models import ExperimentRecord, MarketBarRecord, StrategyVersionRecord, TradeRecordDB
from app.db.session import SessionLocal


def persist_market_bars(symbol: str, bars: list[dict], source: str = "alpaca") -> int:
    session = SessionLocal()
    try:
        count = 0
        for bar in bars:
            session.merge(
                MarketBarRecord(
                    symbol=str(bar.get("symbol", symbol)),
                    timestamp=str(bar.get("timestamp", "")),
                    open=float(bar.get("open", 0.0)),
                    high=float(bar.get("high", 0.0)),
                    low=float(bar.get("low", 0.0)),
                    close=float(bar.get("close", 0.0)),
                    volume=int(bar.get("volume", 0)),
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


def persist_strategy_version(strategy_name: str, version: str, summary: str, *, backtest_return: float = 0.0, walkforward_return: float = 0.0, approved: bool = False) -> dict:
    session = SessionLocal()
    try:
        record = StrategyVersionRecord(
            strategy_name=strategy_name,
            version=version,
            summary=summary,
            status="approved" if approved else "candidate",
            approved=approved,
            backtest_return=backtest_return,
            walkforward_return=walkforward_return,
            created_at="2026-01-01T00:00:00Z",
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return {
            "id": record.id,
            "strategy_name": record.strategy_name,
            "version": record.version,
            "status": record.status,
            "approved": record.approved,
        }
    except Exception:
        return {"id": None, "strategy_name": strategy_name, "version": version, "status": "candidate", "approved": approved}
    finally:
        session.close()


def persist_trade_record(symbol: str, side: str, quantity: int, price: float, strategy_version: str, notes: str = "") -> dict:
    session = SessionLocal()
    try:
        record = TradeRecordDB(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            strategy_version=strategy_version,
            notes=notes,
            timestamp="2026-01-01T00:00:00Z",
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return {
            "id": record.id,
            "symbol": record.symbol,
            "side": record.side,
            "quantity": record.quantity,
            "price": record.price,
            "strategy_version": record.strategy_version,
        }
    except Exception:
        return {"id": None, "symbol": symbol, "side": side, "quantity": quantity, "price": price, "strategy_version": strategy_version}
    finally:
        session.close()


def persist_experiment_result(strategy_name: str, hypothesis: str, baseline_return: float, candidate_return: float, winner: str, status: str) -> dict:
    session = SessionLocal()
    try:
        record = ExperimentRecord(
            experiment_id=f"exp-{abs(hash((strategy_name, hypothesis, baseline_return, candidate_return))) % 1000000}",
            strategy_name=strategy_name,
            hypothesis=hypothesis,
            baseline_return=baseline_return,
            candidate_return=candidate_return,
            winner=winner,
            status=status,
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return {"experiment_id": record.experiment_id, "strategy_name": record.strategy_name, "winner": record.winner, "status": record.status}
    except Exception:
        return {"experiment_id": "demo", "strategy_name": strategy_name, "winner": winner, "status": status}
    finally:
        session.close()
