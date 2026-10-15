from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.experiment_manager import ExperimentManager

router = APIRouter(prefix="/api/v1")

manager = ExperimentManager()


class ExperimentRequest(BaseModel):
    strategy_name: str = Field(..., min_length=1, max_length=64)
    hypothesis: str = Field(..., min_length=1)
    baseline_return: float = Field(default=0.0)
    candidate_return: float = Field(default=0.0)


@router.get("/experiments")
def list_experiments() -> dict[str, list[dict[str, object]]]:
    return {"experiments": [
        {
            "experiment_id": e.experiment_id,
            "strategy_name": e.strategy_name,
            "hypothesis": e.hypothesis,
            "baseline_return": e.baseline_return,
            "candidate_return": e.candidate_return,
            "winner": e.winner,
            "status": e.status,
        }
        for e in manager.list_experiments()
    ]}


@router.post("/experiments/run")
def run_experiment(payload: ExperimentRequest) -> dict[str, object]:
    experiment = manager.run_experiment(
        payload.strategy_name,
        payload.hypothesis,
        payload.baseline_return,
        payload.candidate_return,
    )
    return {
        "experiment_id": experiment.experiment_id,
        "strategy_name": experiment.strategy_name,
        "winner": experiment.winner,
        "status": experiment.status,
    }
