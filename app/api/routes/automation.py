from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.automation import AutomationService

router = APIRouter(prefix="/api/v1")


class AutomationRunRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    closes: list[float] = Field(default_factory=list)
    strategy_name: str = Field(default="moving_average_crossover")


@router.post("/automation/run-cycle")
def run_cycle(payload: AutomationRunRequest) -> dict[str, object]:
    service = AutomationService()
    return service.run_cycle(payload.symbol, payload.closes or None, payload.strategy_name)
