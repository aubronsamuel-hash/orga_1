from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .db import get_session_factory
from .security import decode_jwt

bearer = HTTPBearer(auto_error=False)


def get_db():
    Session = get_session_factory()
    db = Session()
    try:
        yield db
    finally:
        db.close()


def get_current_user_id(cred: HTTPAuthorizationCredentials | None = Depends(bearer)) -> int:
    if cred is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        payload = decode_jwt(cred.credentials)
        if payload.get("typ") != "access":
            raise ValueError("Not access token")
        return int(payload["sub"])
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from err


def require_admin(is_admin: bool) -> None:
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

