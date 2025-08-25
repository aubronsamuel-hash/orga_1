from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...audit import write_audit
from ...db import Base, get_engine
from ...deps import get_current_user_id, get_db
from ...models import Availability
from ...schemas import AvailabilityCreate, AvailabilityOut, AvailabilityUpdate

router = APIRouter(prefix="/availabilities", tags=["availabilities"])


def ensure_tables() -> None:
    Base.metadata.create_all(get_engine())


@router.get("", response_model=list[AvailabilityOut])
def list_availabilities(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    limit: int = Query(1000, ge=1, le=5000),
    offset: int = Query(0, ge=0),
) -> list[AvailabilityOut]:
    ensure_tables()
    rows = db.scalars(
        select(Availability)
        .where(Availability.user_id == user_id)
        .order_by(Availability.start_at)
        .limit(limit)
        .offset(offset)
    ).all()
    return [AvailabilityOut.model_validate(x) for x in rows]


@router.post("", response_model=AvailabilityOut, status_code=201)
def create_availability(
    body: AvailabilityCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> AvailabilityOut:
    ensure_tables()
    a = Availability(user_id=user_id, start_at=body.start_at, end_at=body.end_at, note=body.note)
    if a.end_at <= a.start_at:
        raise HTTPException(status_code=422, detail="end_at doit etre > start_at")
    db.add(a)
    db.commit()
    db.refresh(a)
    write_audit(db, actor_user_id=user_id, action="availability.create", entity="availability", entity_id=str(a.id), details={})
    return AvailabilityOut.model_validate(a)


@router.patch("/{aid}", response_model=AvailabilityOut)
def update_availability(
    aid: int,
    body: AvailabilityUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> AvailabilityOut:
    ensure_tables()
    a = db.get(Availability, aid)
    if not a or a.user_id != user_id:
        raise HTTPException(status_code=404, detail="Availability introuvable")
    if body.start_at is not None:
        a.start_at = body.start_at
    if body.end_at is not None:
        a.end_at = body.end_at
    if body.note is not None:
        a.note = body.note
    if a.end_at <= a.start_at:
        raise HTTPException(status_code=422, detail="end_at doit etre > start_at")
    db.commit()
    db.refresh(a)
    write_audit(db, actor_user_id=user_id, action="availability.update", entity="availability", entity_id=str(a.id), details={})
    return AvailabilityOut.model_validate(a)


@router.delete("/{aid}", status_code=204)
def delete_availability(
    aid: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> None:
    ensure_tables()
    a = db.get(Availability, aid)
    if not a or a.user_id != user_id:
        raise HTTPException(status_code=404, detail="Availability introuvable")
    db.delete(a)
    db.commit()
    write_audit(db, actor_user_id=user_id, action="availability.delete", entity="availability", entity_id=str(aid), details={})
    return None

