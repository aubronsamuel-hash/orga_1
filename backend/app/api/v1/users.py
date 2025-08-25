from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...deps import get_current_user_id, get_db, require_admin
from ...models import User
from ...schemas import UserCreate, UserOut, UserUpdate
from ...security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def me(
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> UserOut:
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(u)


@router.get("", response_model=list[UserOut])
def list_users(
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> list[UserOut]:
    u = db.get(User, user_id)
    require_admin(u.is_admin if u else False)
    rows = db.scalars(select(User).limit(limit).offset(offset)).all()
    return [UserOut.model_validate(x) for x in rows]


@router.post("", response_model=UserOut, status_code=201)
def create_user(
    body: UserCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> UserOut:
    u = db.get(User, user_id)
    require_admin(u.is_admin if u else False)
    exists = db.scalar(select(User).where(User.email == body.email.lower()))
    if exists:
        raise HTTPException(status_code=409, detail="email deja utilise")
    nu = User(email=body.email.lower(), password_hash=hash_password(body.password))
    db.add(nu)
    db.commit()
    db.refresh(nu)
    return UserOut.model_validate(nu)


@router.patch("/{uid}", response_model=UserOut)
def update_user(
    uid: int,
    body: UserUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> UserOut:
    u = db.get(User, user_id)
    require_admin(u.is_admin if u else False)
    target = db.get(User, uid)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    if body.is_active is not None:
        target.is_active = body.is_active
    if body.is_admin is not None:
        target.is_admin = body.is_admin
    db.commit()
    db.refresh(target)
    return UserOut.model_validate(target)


@router.delete("/{uid}", status_code=204)
def delete_user(
    uid: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    u = db.get(User, user_id)
    require_admin(u.is_admin if u else False)
    target = db.get(User, uid)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(target)
    db.commit()
    return None

