import pytest
from fastapi.testclient import TestClient
import sys
sys.path.append('..')
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_fetch_trends():
    payload = {
        "keywords": ["python", "javascript"],
        "timeframe": "today 3-m",
        "geo": ""
    }
    response = client.post("/api/fetch-trends", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
