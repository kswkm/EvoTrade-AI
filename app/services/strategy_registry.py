from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StrategyVersion:
    name: str
    version: str
    status: str
    summary: str
    created_at: str
    backtest_return: float = 0.0
    walkforward_return: float = 0.0
    approved: bool = False


@dataclass
class StrategyRegistry:
    versions: dict[str, StrategyVersion] = field(default_factory=dict)

    def register(self, strategy_name: str, version: str, summary: str, *, backtest_return: float = 0.0, walkforward_return: float = 0.0, approved: bool = False) -> StrategyVersion:
        key = f"{strategy_name}:{version}"
        item = StrategyVersion(
            name=strategy_name,
            version=version,
            status="approved" if approved else "candidate",
            summary=summary,
            created_at="2026-01-01T00:00:00Z",
            backtest_return=backtest_return,
            walkforward_return=walkforward_return,
            approved=approved,
        )
        self.versions[key] = item
        return item

    def list_versions(self) -> list[StrategyVersion]:
        return list(self.versions.values())

    def get_latest(self, strategy_name: str) -> StrategyVersion | None:
        matches = [v for v in self.versions.values() if v.name == strategy_name]
        return matches[-1] if matches else None
