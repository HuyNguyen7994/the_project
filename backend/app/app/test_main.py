from fastapi.testclient import TestClient
from .main import app
import json

client = TestClient(app)


def test_check_health():
    response = client.get("api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_message():
    response = client.post("api/v1/message/Tester", json={"content": "Hello World"})
    assert response.status_code == 200
    assert response.json() == {"sender": "Tester", "content" :"Hello World"}