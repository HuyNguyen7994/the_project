from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_check_health():
    response = client.get("api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}