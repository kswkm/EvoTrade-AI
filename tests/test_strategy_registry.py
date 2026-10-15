from app.services.strategy_registry import StrategyRegistry


def test_strategy_registry_registers_versions():
    registry = StrategyRegistry()
    version = registry.register("moving_average_crossover", "v1", "baseline strategy", backtest_return=0.12, walkforward_return=0.08, approved=True)
    assert version.name == "moving_average_crossover"
    assert version.status == "approved"
    assert registry.get_latest("moving_average_crossover").version == "v1"
