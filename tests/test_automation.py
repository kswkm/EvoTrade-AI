from app.services.automation import AutomationService


def test_automation_cycle_runs_for_valid_series():
    service = AutomationService()
    result = service.run_cycle("AAPL", [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114])
    assert result["status"] == "ok"
    assert result["symbol"] == "AAPL"
    assert "approved" in result
