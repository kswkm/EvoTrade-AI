from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_historical_market_endpoint_returns_valid_bars():
    response = client.post("/api/v1/market/historical", json={"symbol": "AAPL", "limit": 4})
    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "AAPL"
    assert payload["valid"] is True
    assert payload["count"] == 4
    assert len(payload["bars"]) == 4
