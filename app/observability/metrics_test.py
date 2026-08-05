from fastapi import status
from fastapi.testclient import TestClient
from app import main

def test_unsecured_metrics_endpoint_request(monkeypatch):
    """Metric endpoint shouldn't accessible without a legit basic-auth"""

    monkeypatch.setenv("PASTORE_METRICS_ENABLED", "true")
    monkeypatch.setenv("PASTORE_METRICS_USERNAME", "parsa")
    monkeypatch.setenv("PASTORE_METRICS_PASSWORD", "123456")

    client = TestClient(main.create_app())

    response = client.get(
        "/metrics",
        auth=("parsa","123456"),
    )

    assert response.status_code == status.HTTP_200_OK


    response = client.get(
        "/metrics",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_secured_metrics_endpoint_request(monkeypatch):
    """Metric endpoint should be accessible without auth, if the username or password were empty."""

    monkeypatch.setenv("PASTORE_METRICS_ENABLED", "true")
    monkeypatch.setenv("PASTORE_METRICS_USERNAME", "") 
    monkeypatch.setenv("PASTORE_METRICS_PASSWORD", "")

    client = TestClient(main.create_app())

    response = client.get(
        "/metrics",
    )

    assert response.status_code == status.HTTP_200_OK
