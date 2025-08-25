from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from hypothesis import given, settings, strategies as st

from app.main import app


def auth(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={"email": "vv@example.com", "password": "Passw0rd!"},
    )
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "vv@example.com", "password": "Passw0rd!"},
    )
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_mission_invalid_dates_422():
    c = TestClient(app)
    h = auth(c)
    now = datetime.now(UTC)
    r = c.post(
        "/api/v1/missions",
        headers=h,
        json={"title": "X", "start_at": now.isoformat(), "end_at": now.isoformat()},
    )
    assert r.status_code == 422


@given(
    start_ts=st.integers(min_value=1_700_000_000, max_value=2_000_000_000),
    dur=st.integers(min_value=1, max_value=24 * 3600),
)
def test_property_mission_dates_ok(start_ts, dur):
    c = TestClient(app)
    h = auth(c)
    start = datetime.fromtimestamp(start_ts, tz=UTC)
    end = start + timedelta(seconds=dur)
    r = c.post(
        "/api/v1/missions",
        headers=h,
        json={"title": "P", "start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert r.status_code == 201


def test_assignment_overlap_409():
    c = TestClient(app)
    h = auth(c)
    now = datetime.now(UTC)
    start = now + timedelta(days=1)
    end = start + timedelta(hours=8)
    # mission A
    ma = c.post(
        "/api/v1/missions",
        headers=h,
        json={"title": "A", "start_at": start.isoformat(), "end_at": end.isoformat()},
    ).json()
    me = c.get("/api/v1/users/me", headers=h).json()
    a1start = start + timedelta(hours=1)
    a1end = a1start + timedelta(hours=4)
    a2start = a1start + timedelta(hours=2)  # overlap
    a2end = a2start + timedelta(hours=3)
    r1 = c.post(
        f"/api/v1/missions/{ma['id']}/assignments",
        headers=h,
        json={
            "user_id": me["id"],
            "start_at": a1start.isoformat(),
            "end_at": a1end.isoformat(),
        },
    )
    assert r1.status_code == 201
    r2 = c.post(
        f"/api/v1/missions/{ma['id']}/assignments",
        headers=h,
        json={
            "user_id": me["id"],
            "start_at": a2start.isoformat(),
            "end_at": a2end.isoformat(),
        },
    )
    assert r2.status_code == 409
settings.register_profile("ci", deadline=None)
settings.load_profile("ci")
