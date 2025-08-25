from fastapi.testclient import TestClient

from app.main import app


def test_rate_limit_login_triggers_429():
    c = TestClient(app)
    c.post("/api/v1/auth/register", json={"email": "rl@example.com", "password": "passw0rd!"})
    # Do many wrong attempts
    hits = 0
    status_codes = []
    for _ in range(10):
        r = c.post("/api/v1/auth/login", json={"email": "rl@example.com", "password": "bad"})
        hits += 1
        status_codes.append(r.status_code)
        if r.status_code == 429:
            break
    assert 429 in status_codes

