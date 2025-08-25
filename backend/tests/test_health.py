from fastapi.testclient import TestClient

from app.main import app


def test_health_ok():
    client = TestClient(app)
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "time_utc" in body


def test_version_ok():
    client = TestClient(app)
    r = client.get("/api/v1/version")
    assert r.status_code == 200
    body = r.json()
    assert "version" in body and "git_sha" in body

