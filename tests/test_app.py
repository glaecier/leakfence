from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "LeakFence" in response.text
    assert "Production deployment is protected" in response.text


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
