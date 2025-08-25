from fastapi.testclient import TestClient

from app.main import app


def register_and_login(client: TestClient, email: str, password: str) -> tuple[str, str]:
    r = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert r.status_code in (201, 409)
    r = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    body = r.json()
    return body["access_token"], body["refresh_token"]


def test_register_login_refresh_logout_ok():
    c = TestClient(app)
    access, refresh = register_and_login(c, "a@example.com", "passw0rd!")
    # /users/me
    r = c.get("/api/v1/users/me", headers={"Authorization": f"Bearer {access}"})
    assert r.status_code == 200
    me = r.json()
    assert me["email"] == "a@example.com"

    # refresh rotation
    r = c.post("/api/v1/auth/refresh", params={"refresh_token": refresh})
    assert r.status_code == 200
    body = r.json()
    assert body["access_token"] and body["refresh_token"]
    # old refresh should be revoked after logout
    r2 = c.post("/api/v1/auth/logout", params={"refresh_token": refresh})
    assert r2.status_code == 204
    r3 = c.post("/api/v1/auth/refresh", params={"refresh_token": refresh})
    assert r3.status_code == 401


def test_login_bad_password_401():
    c = TestClient(app)
    c.post("/api/v1/auth/register", json={"email": "b@example.com", "password": "passw0rd!"})
    r = c.post("/api/v1/auth/login", json={"email": "b@example.com", "password": "bad"})
    assert r.status_code == 401


def test_me_requires_auth_401():
    c = TestClient(app)
    r = c.get("/api/v1/users/me")
    assert r.status_code == 401

