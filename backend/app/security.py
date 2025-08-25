import hashlib
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

import jwt
from passlib.context import CryptContext

from .config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    s = get_settings()
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_jwt(payload: Dict[str, Any], ttl_seconds: int) -> str:
    s = get_settings()
    to_encode = {**payload, "iat": int(time.time()), "exp": int(time.time()) + ttl_seconds}
    return jwt.encode(to_encode, s.jwt_secret, algorithm=s.jwt_alg)


def decode_jwt(token: str) -> Dict[str, Any]:
    s = get_settings()
    return jwt.decode(token, s.jwt_secret, algorithms=[s.jwt_alg])


def make_access_token(user_id: int) -> str:
    s = get_settings()
    return create_jwt({"sub": str(user_id), "typ": "access"}, s.access_ttl_seconds)


def make_refresh_token(user_id: int) -> str:
    s = get_settings()
    return create_jwt({"sub": str(user_id), "typ": "refresh", "jti": str(uuid4())}, s.refresh_ttl_seconds)


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


