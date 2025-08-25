from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...config import get_settings
from ...db import Base, get_engine
from ...deps import get_current_user_id, get_db
from ...models import RefreshToken, User
from ...rate_limit import check_and_inc
from ...schemas import LoginIn, TokenPair, UserCreate, UserOut
from ...security import (
    hash_password,
    make_access_token,
    make_refresh_token,
    sha256_hex,
    verify_password,
)

router = APIRouter(tags=["auth"])


def ensure_tables() -> None:
    # Simple create_all for J3 (Alembic viendra plus tard)
    Base.metadata.create_all(get_engine())


@router.post("/auth/register", response_model=UserOut, status_code=201)
def register(
    user_in: UserCreate, db: Annotated[Session, Depends(get_db)]
) -> UserOut:
    ensure_tables()
    existing = db.scalar(select(User).where(User.email == user_in.email.lower()))
    if existing:
        raise HTTPException(status_code=409, detail="email deja utilise")
    u = User(email=user_in.email.lower(), password_hash=hash_password(user_in.password))
    db.add(u)
    db.commit()
    db.refresh(u)
    return UserOut.model_validate(u)


@router.post("/auth/login", response_model=TokenPair)
def login(
    body: LoginIn,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> TokenPair:
    ensure_tables()
    s = get_settings()
    ip = request.client.host if request.client else "unknown"
    if not check_and_inc(f"ip:{ip}") or not check_and_inc(f"user:{body.email.lower()}"):
        raise HTTPException(status_code=429, detail="Trop de tentatives, reessayez plus tard")

    u = db.scalar(select(User).where(User.email == body.email.lower()))
    if u is None or not verify_password(body.password, u.password_hash):
        if u is not None:
            u.failed_login_attempts += 1
            if u.failed_login_attempts >= s.auth_max_fails:
                u.locked_until = datetime.now(UTC) + timedelta(minutes=s.auth_lock_minutes)
                u.failed_login_attempts = 0
            db.commit()
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    assert u is not None

    if u.locked_until and datetime.now(UTC) < u.locked_until:
        raise HTTPException(status_code=423, detail="Compte verrouille, reessayez plus tard")

    if u.totp_enabled:
        if (body.totp_code or "").strip() != "000000":
            raise HTTPException(status_code=401, detail="TOTP requis ou invalide")

    # Reset counters on success
    u.failed_login_attempts = 0
    u.locked_until = None
    db.commit()

    access = make_access_token(u.id)
    refresh = make_refresh_token(u.id)

    rt = RefreshToken(
        user_id=u.id,
        token_hash=sha256_hex(refresh),
        expires_at=datetime.utcnow() + timedelta(seconds=s.refresh_ttl_seconds),
        revoked=False,
    )
    db.add(rt)
    db.commit()

    return TokenPair(access_token=access, refresh_token=refresh, expires_in=s.access_ttl_seconds)


@router.post("/auth/refresh", response_model=TokenPair)
def refresh_token(
    refresh_token: str, db: Annotated[Session, Depends(get_db)]
) -> TokenPair:
    ensure_tables()
    s = get_settings()
    # We do not decode refresh JWT here to keep rotation strict: we trust DB blacklist
    h = sha256_hex(refresh_token)
    rt = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == h))
    if not rt or rt.revoked or rt.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh invalide")
    # rotate: revoke current and issue new pair
    rt.revoked = True
    db.commit()

    u = db.get(User, rt.user_id)
    if not u or not u.is_active:
        raise HTTPException(status_code=401, detail="Utilisateur inactif")

    access = make_access_token(u.id)
    new_refresh = make_refresh_token(u.id)
    new_rt = RefreshToken(
        user_id=u.id,
        token_hash=sha256_hex(new_refresh),
        expires_at=datetime.utcnow() + timedelta(seconds=s.refresh_ttl_seconds),
        revoked=False,
    )
    db.add(new_rt)
    db.commit()
    return TokenPair(
        access_token=access,
        refresh_token=new_refresh,
        expires_in=s.access_ttl_seconds,
    )


@router.post("/auth/logout", status_code=204)
def logout(refresh_token: str, db: Annotated[Session, Depends(get_db)]) -> None:
    ensure_tables()
    h = sha256_hex(refresh_token)
    rt = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == h))
    if rt:
        rt.revoked = True
        db.commit()
    return None


@router.post("/auth/2fa/enable", status_code=204)
def enable_2fa(
    _: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    # Stub: just flag enabled, secret placeholder
    ensure_tables()

    u = db.get(User, _)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    u.totp_enabled = True
    u.totp_secret = "stub"
    db.commit()
    return None

