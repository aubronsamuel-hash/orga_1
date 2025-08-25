from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.main import app


def auth(client: TestClient, email="conf@example.com", pwd="Passw0rd!"):
    client.post("/api/v1/auth/register", json={"email": email, "password": pwd})
    r = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}, r.json()["access_token"]


def test_conflicts_basic():
    c = TestClient(app)
    h, _ = auth(c)

    now = datetime.now(UTC)
    m_start = now + timedelta(days=2)
    m_end = m_start + timedelta(hours=8)

    # creer mission
    r = c.post("/api/v1/missions", headers=h, json={"title": "Show", "start_at": m_start.isoformat(), "end_at": m_end.isoformat()})
    assert r.status_code == 201, r.text
    mid = r.json()["id"]

    # me
    me = c.get("/api/v1/users/me", headers=h).json()

    # assignment pour 10-12h
    a_start = m_start + timedelta(hours=2)
    a_end = a_start + timedelta(hours=2)
    r = c.post(f"/api/v1/missions/{mid}/assignments", headers=h, json={"user_id": me["id"], "start_at": a_start.isoformat(), "end_at": a_end.isoformat()})
    assert r.status_code == 201

    # aucun dispo -> conflit present
    r = c.get("/api/v1/conflicts", headers=h)
    assert r.status_code == 200
    confs = r.json()
    assert any(c["mission_id"] == mid for c in confs)

    # ajouter une availability couvrant integralement -> plus de conflit
    r = c.post("/api/v1/availabilities", headers=h, json={"start_at": m_start.isoformat(), "end_at": m_end.isoformat(), "note": "journee"})
    assert r.status_code == 201

    r = c.get("/api/v1/conflicts", headers=h)
    assert r.status_code == 200
    confs2 = r.json()
    assert not any(c["mission_id"] == mid for c in confs2)

