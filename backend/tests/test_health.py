"""
Tests for System Health Endpoint.
Product: SCANNAI | Team: ROCKERZ
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint_returns_200():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data
    assert "ingestion_status" in data


def test_health_endpoint_does_not_leak_secrets():
    response = client.get("/api/v1/health")
    data_str = response.text.lower()
    # Ensure sensitive tokens or system variables are never leaked
    assert "key" not in data_str or "api_key" not in data_str
    assert "password" not in data_str
    assert "token" not in data_str
    assert "secret" not in data_str


def test_root_endpoint_beacon():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "/api/v1/health" in data["api_v1"]
