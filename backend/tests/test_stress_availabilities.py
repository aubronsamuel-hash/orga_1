from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.db import Base, get_engine, session_scope
from app.main import app
from app.models import Availability


def test_stress_bulk_1000_dispos_ok():
    c = TestClient(app)
    # register/login pour obtenir user_id
    c.post("/api/v1/auth/register", json={"email": "bulk@example.com", "password": "Passw0rd!"})
    r = c.post("/api/v1/auth/login", json={"email": "bulk@example.com", "password": "Passw0rd!"})
    h = {"Authorization": f"Bearer {r.json()['access_token']}"}
    me = c.get("/api/v1/users/me", headers=h).json()
    uid = me["id"]

    # insertion bulk directe (plus rapide que 1000 POST)
    now = datetime.now(UTC)
    Base.metadata.create_all(get_engine())
    with session_scope() as s:
        arr = []
        for i in range(1000):
            start = now + timedelta(days=i//8, hours=(i % 8) * 3)
            end = start + timedelta(hours=2)
            arr.append(Availability(user_id=uid, start_at=start, end_at=end, note=f"slot{i}"))
        s.bulk_save_objects(arr)

    # listing doit renvoyer >= 1000
    r = c.get("/api/v1/availabilities", headers=h)
    assert r.status_code == 200
    assert len(r.json()) >= 1000

