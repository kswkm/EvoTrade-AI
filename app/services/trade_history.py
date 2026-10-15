from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TradeRecord:
    symbol: str
    side: str
    quantity: int
    price: float
    strategy_version: str
    timestamp: str
    notes: str = ""


@dataclass
class TradeHistory:
    records: list[TradeRecord] = field(default_factory=list)

    def add_record(self, symbol: str, side: str, quantity: int, price: float, strategy_version: str, notes: str = "") -> TradeRecord:
        record = TradeRecord(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            strategy_version=strategy_version,
            timestamp="2026-01-01T00:00:00Z",
            notes=notes,
        )
        self.records.append(record)
        return record

    def list_records(self) -> list[TradeRecord]:
        return list(self.records)
