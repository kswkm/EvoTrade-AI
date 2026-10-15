from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_system_status_and_overview_endpoints():
    response = client.get("/api/v1/system/status")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["mode"] == "paper_trading_only"
    assert payload["risk_engine"] == "enabled"
    assert "scheduler" in payload
    assert "features" in payload

    overview = client.get("/api/v1/system/overview")
    assert overview.status_code == 200
    assert overview.json()["status"] == "ready"


def test_scheduler_start_and_stop_routes():
    response = client.post("/api/v1/system/scheduler/start", json={"symbol": "AAPL", "interval_seconds": 30})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] in {"started", "already_running"}

    stop = client.post("/api/v1/system/scheduler/stop")
    assert stop.status_code == 200
    assert stop.json()["status"] == "stopped"
