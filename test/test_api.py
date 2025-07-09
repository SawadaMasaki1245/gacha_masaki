from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_single_gacha_api():
    response = client.get("/gacha/single")
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "count" in data

def test_ten_gacha_api():
    response = client.get("/gacha/ten")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data.get("results"), list)
    assert len(data["results"]) == 10
    assert "count" in data