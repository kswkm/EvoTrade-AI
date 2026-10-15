from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ExperimentResult:
    experiment_id: str
    strategy_name: str
    hypothesis: str
    baseline_return: float
    candidate_return: float
    winner: str
    status: str


@dataclass
class ExperimentManager:
    experiments: list[ExperimentResult] = field(default_factory=list)

    def run_experiment(self, strategy_name: str, hypothesis: str, baseline_return: float, candidate_return: float) -> ExperimentResult:
        winner = "candidate" if candidate_return >= baseline_return else "baseline"
        status = "approved" if winner == "candidate" else "rejected"
        experiment = ExperimentResult(
            experiment_id=f"exp-{len(self.experiments) + 1}",
            strategy_name=strategy_name,
            hypothesis=hypothesis,
            baseline_return=baseline_return,
            candidate_return=candidate_return,
            winner=winner,
            status=status,
        )
        self.experiments.append(experiment)
        return experiment

    def list_experiments(self) -> list[ExperimentResult]:
        return list(self.experiments)
