from fastapi.testclient import TestClient

from app.main import app


def test_404_returns_json_error():
    client = TestClient(app)
    r = client.get("/api/v1/unknown")
    assert r.status_code == 404
    body = r.json()
    assert "error" in body and body["error"]["code"] == "HTTP_404"

