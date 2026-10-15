from app.services.experiment_manager import ExperimentManager


def test_experiment_manager_tracks_candidate_success():
    manager = ExperimentManager()
    experiment = manager.run_experiment("moving_average_crossover", "filter volatility", 0.04, 0.08)
    assert experiment.winner == "candidate"
    assert experiment.status == "approved"
    assert len(manager.list_experiments()) == 1
