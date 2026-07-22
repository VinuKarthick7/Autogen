import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    
def test_create_run():
    response = client.post("/runs", json={
        "repository_path": "./pinesphere_backend",
        "feature_request": "Add loyalty rewards"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"
    assert "run_id" in data
    
def test_list_runs():
    response = client.get("/runs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
