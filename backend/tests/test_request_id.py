from fastapi.testclient import TestClient

from app.main import app


def test_request_id_propagates_when_provided():
    client = TestClient(app)
    rid = "test-req-123"
    r = client.get("/api/v1/health", headers={"X-Request-ID": rid})
    assert r.status_code == 200
    assert r.headers.get("X-Request-ID") == rid


def test_request_id_generated_when_absent():
    client = TestClient(app)
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    rid = r.headers.get("X-Request-ID")
    assert isinstance(rid, str) and len(rid) > 0

