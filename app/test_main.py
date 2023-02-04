from app import main
from fastapi import testclient

client = testclient.TestClient(main.app)

def test_healthcheck():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Truckin'"}
