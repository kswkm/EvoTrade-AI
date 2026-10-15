from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.strategy_registry import StrategyRegistry

router = APIRouter(prefix="/api/v1")


class StrategyVersionRequest(BaseModel):
    strategy_name: str = Field(..., min_length=1, max_length=64)
    version: str = Field(default="v1")
    summary: str = Field(default="candidate strategy")
    backtest_return: float = 0.0
    walkforward_return: float = 0.0
    approved: bool = False


registry = StrategyRegistry()


@router.get("/strategies/versions")
def list_versions() -> dict[str, list[dict[str, object]]]:
    return {"versions": [
        {
            "name": v.name,
            "version": v.version,
            "status": v.status,
            "summary": v.summary,
            "approved": v.approved,
            "backtest_return": v.backtest_return,
            "walkforward_return": v.walkforward_return,
        }
        for v in registry.list_versions()
    ]}


@router.post("/strategies/register")
def register_strategy(payload: StrategyVersionRequest) -> dict[str, object]:
    version = registry.register(
        payload.strategy_name,
        payload.version,
        payload.summary,
        backtest_return=payload.backtest_return,
        walkforward_return=payload.walkforward_return,
        approved=payload.approved,
    )
    return {
        "name": version.name,
        "version": version.version,
        "status": version.status,
        "approved": version.approved,
    }
