from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.main import app


def auth(client: TestClient, email="avail@example.com", pwd="Passw0rd!"):
    client.post("/api/v1/auth/register", json={"email": email, "password": pwd})
    r = client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert r.status_code == 200
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_availability_crud_and_utc():
    c = TestClient(app)
    h = auth(c)
    # naive -> traite comme UTC
    start = datetime(2025, 1, 1, 8, 0, 0)  # naive
    end = start + timedelta(hours=4)
    r = c.post("/api/v1/availabilities", headers=h, json={"start_at": start.isoformat(), "end_at": end.isoformat(), "note": "am"})
    assert r.status_code == 201, r.text
    a = r.json()
    assert a["note"] == "am"
    assert a["start_at"].endswith("+00:00")
    aid = a["id"]

    # list
    r = c.get("/api/v1/availabilities", headers=h)
    assert r.status_code == 200
    arr = r.json()
    assert any(x["id"] == aid for x in arr)

    # patch
    r = c.patch(f"/api/v1/availabilities/{aid}", headers=h, json={"note": "am2"})
    assert r.status_code == 200
    assert r.json()["note"] == "am2"

    # delete
    r = c.delete(f"/api/v1/availabilities/{aid}", headers=h)
    assert r.status_code == 204

