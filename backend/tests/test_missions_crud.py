from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app


def auth(client: TestClient, email="u@example.com", pwd="Passw0rd!"):
    client.post("/api/v1/auth/register", json={"email": email, "password": pwd})
    r = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert r.status_code == 200
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_mission_crud_ok():
    c = TestClient(app)
    h = auth(c)

    start = datetime.now(timezone.utc) + timedelta(days=1)
    end = start + timedelta(hours=8)

    r = c.post("/api/v1/missions", headers=h, json={"title": "Montage", "location": "Bobino", "start_at": start.isoformat(), "end_at": end.isoformat()})
    assert r.status_code == 201, r.text
    mid = r.json()["id"]

    # read
    r = c.get(f"/api/v1/missions/{mid}", headers=h)
    assert r.status_code == 200
    assert r.json()["title"] == "Montage"

    # update
    r = c.patch(f"/api/v1/missions/{mid}", headers=h, json={"location": "Bobino - Cour"})
    assert r.status_code == 200
    assert r.json()["location"] == "Bobino - Cour"

    # roles
    r = c.post(f"/api/v1/missions/{mid}/roles", headers=h, json={"name": "Son", "quantity": 2})
    assert r.status_code == 201
    rid = r.json()["id"]

    # assignments
    a_start = start + timedelta(hours=1)
    a_end = a_start + timedelta(hours=4)
    # Need a user to assign: reuse same user id by calling /users/me
    me = c.get("/api/v1/users/me", headers=h).json()
    r = c.post(f"/api/v1/missions/{mid}/assignments", headers=h, json={"user_id": me["id"], "role_id": rid, "start_at": a_start.isoformat(), "end_at": a_end.isoformat()})
    assert r.status_code == 201

    # delete assignment
    aid = r.json()["id"]
    r = c.delete(f"/api/v1/missions/{mid}/assignments/{aid}", headers=h)
    assert r.status_code == 204

    # delete role
    r = c.delete(f"/api/v1/missions/{mid}/roles/{rid}", headers=h)
    assert r.status_code == 204

    # delete mission
    r = c.delete(f"/api/v1/missions/{mid}", headers=h)
    assert r.status_code == 204
