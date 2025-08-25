from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...audit import write_audit
from ...deps import get_current_user_id, get_db
from ...models import Assignment, Mission, MissionRole
from ...schemas import (
    AssignmentCreate,
    AssignmentOut,
    MissionCreate,
    MissionDetail,
    MissionOut,
    MissionRoleCreate,
    MissionRoleOut,
    MissionRoleUpdate,
    MissionUpdate,
    _norm_utc,
)

router = APIRouter(prefix="/missions", tags=["missions"])


def _ensure_bounds(m: Mission) -> None:
    if m.end_at <= m.start_at:
        raise HTTPException(status_code=422, detail="end_at doit etre > start_at")


def _role_inside_mission(m: Mission, start_at: datetime | None, end_at: datetime | None) -> None:
    if start_at and start_at < m.start_at:
        raise HTTPException(status_code=422, detail="role.start_at hors mission")
    if end_at and end_at > m.end_at:
        raise HTTPException(status_code=422, detail="role.end_at hors mission")
    if start_at and end_at and end_at <= start_at:
        raise HTTPException(status_code=422, detail="role.end_at doit etre > role.start_at")


def _assignment_inside_mission(m: Mission, start_at: datetime, end_at: datetime) -> None:
    s = _norm_utc(start_at)
    e = _norm_utc(end_at)
    ms = _norm_utc(m.start_at)
    me = _norm_utc(m.end_at)
    if s < ms or e > me:
        raise HTTPException(status_code=422, detail="assignment hors mission")
    if e <= s:
        raise HTTPException(status_code=422, detail="assignment end_at doit etre > start_at")


def _overlap_exists(
    db: Session,
    user_id: int,
    start_at: datetime,
    end_at: datetime,
    exclude_id: int | None = None,
) -> bool:
    s = _norm_utc(start_at)
    e = _norm_utc(end_at)
    q = select(Assignment).where(
        Assignment.user_id == user_id,
        Assignment.start_at < e,
        Assignment.end_at > s,
    )
    if exclude_id:
        q = q.where(Assignment.id != exclude_id)
    return db.scalar(q.limit(1)) is not None


@router.get("", response_model=list[MissionOut])
def list_missions(
    _: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> list[MissionOut]:
    rows = (
        db.scalars(
            select(Mission)
                .order_by(Mission.start_at.desc())
                .limit(limit)
                .offset(offset)
        ).all()
    )
    return [MissionOut.model_validate(x) for x in rows]


@router.post("", response_model=MissionOut, status_code=201)
def create_mission(
    body: MissionCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> MissionOut:
    m = Mission(
        title=body.title,
        location=body.location,
        start_at=body.start_at,
        end_at=body.end_at,
        description=body.description,
    )
    _ensure_bounds(m)
    db.add(m)
    db.commit()
    db.refresh(m)
    write_audit(
        db,
        actor_user_id=user_id,
        action="mission.create",
        entity="mission",
        entity_id=str(m.id),
        details={"title": m.title},
    )
    return MissionOut.model_validate(m)


@router.get("/{mid}", response_model=MissionDetail)
def get_mission(
    _: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    mid: int = Path(..., ge=1),
) -> MissionDetail:
    m = db.get(Mission, mid)
    if not m:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    roles = db.scalars(select(MissionRole).where(MissionRole.mission_id == m.id)).all()
    assigns = db.scalars(select(Assignment).where(Assignment.mission_id == m.id)).all()
    return MissionDetail.model_validate(
        {
            "id": m.id,
            "title": m.title,
            "location": m.location,
            "start_at": m.start_at,
            "end_at": m.end_at,
            "description": m.description,
            "roles": [MissionRoleOut.model_validate(r).model_dump() for r in roles],
            "assignments": [AssignmentOut.model_validate(a).model_dump() for a in assigns],
        }
    )


@router.patch("/{mid}", response_model=MissionOut)
def update_mission(
    mid: int,
    body: MissionUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> MissionOut:
    m = db.get(Mission, mid)
    if not m:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    if body.title is not None:
        m.title = body.title
    if body.location is not None:
        m.location = body.location
    if body.start_at is not None:
        m.start_at = body.start_at
    if body.end_at is not None:
        m.end_at = body.end_at
    if body.description is not None:
        m.description = body.description
    _ensure_bounds(m)
    db.commit()
    db.refresh(m)
    write_audit(
        db,
        actor_user_id=user_id,
        action="mission.update",
        entity="mission",
        entity_id=str(m.id),
        details={"title": m.title},
    )
    return MissionOut.model_validate(m)


@router.delete("/{mid}", status_code=204)
def delete_mission(
    mid: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    m = db.get(Mission, mid)
    if not m:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    db.delete(m)
    db.commit()
    write_audit(
        db,
        actor_user_id=user_id,
        action="mission.delete",
        entity="mission",
        entity_id=str(mid),
        details={},
    )
    return None


# --- Roles ---

@router.get("/{mid}/roles", response_model=list[MissionRoleOut])
def list_roles(
    mid: int,
    _: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> list[MissionRoleOut]:
    if not db.get(Mission, mid):
        raise HTTPException(status_code=404, detail="Mission introuvable")
    rows = db.scalars(select(MissionRole).where(MissionRole.mission_id == mid)).all()
    return [MissionRoleOut.model_validate(r) for r in rows]


@router.post("/{mid}/roles", response_model=MissionRoleOut, status_code=201)
def create_role(
    mid: int,
    body: MissionRoleCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> MissionRoleOut:
    m = db.get(Mission, mid)
    if not m:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    _role_inside_mission(m, body.start_at, body.end_at)
    r = MissionRole(
        mission_id=mid,
        name=body.name,
        start_at=body.start_at,
        end_at=body.end_at,
        quantity=body.quantity,
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    write_audit(
        db,
        actor_user_id=user_id,
        action="role.create",
        entity="role",
        entity_id=str(r.id),
        details={"mission_id": mid},
    )
    return MissionRoleOut.model_validate(r)


@router.patch("/{mid}/roles/{rid}", response_model=MissionRoleOut)
def update_role(
    mid: int,
    rid: int,
    body: MissionRoleUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> MissionRoleOut:
    m = db.get(Mission, mid)
    if not m:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    r = db.get(MissionRole, rid)
    if not r or r.mission_id != mid:
        raise HTTPException(status_code=404, detail="Role introuvable")
    start = body.start_at if body.start_at is not None else r.start_at
    end = body.end_at if body.end_at is not None else r.end_at
    _role_inside_mission(m, start, end)

    if body.name is not None:
        r.name = body.name
    if body.start_at is not None:
        r.start_at = body.start_at
    if body.end_at is not None:
        r.end_at = body.end_at
    if body.quantity is not None:
        r.quantity = body.quantity
    db.commit()
    db.refresh(r)
    write_audit(
        db,
        actor_user_id=user_id,
        action="role.update",
        entity="role",
        entity_id=str(r.id),
        details={"mission_id": mid},
    )
    return MissionRoleOut.model_validate(r)


@router.delete("/{mid}/roles/{rid}", status_code=204)
def delete_role(
    mid: int,
    rid: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    r = db.get(MissionRole, rid)
    if not r or r.mission_id != mid:
        raise HTTPException(status_code=404, detail="Role introuvable")
    db.delete(r)
    db.commit()
    write_audit(
        db,
        actor_user_id=user_id,
        action="role.delete",
        entity="role",
        entity_id=str(rid),
        details={"mission_id": mid},
    )
    return None


# --- Assignments ---

@router.get("/{mid}/assignments", response_model=list[AssignmentOut])
def list_assignments(
    mid: int,
    _: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> list[AssignmentOut]:
    if not db.get(Mission, mid):
        raise HTTPException(status_code=404, detail="Mission introuvable")
    rows = db.scalars(select(Assignment).where(Assignment.mission_id == mid)).all()
    return [AssignmentOut.model_validate(a) for a in rows]


@router.post("/{mid}/assignments", response_model=AssignmentOut, status_code=201)
def create_assignment(
    mid: int,
    body: AssignmentCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> AssignmentOut:
    m = db.get(Mission, mid)
    if not m:
        raise HTTPException(status_code=404, detail="Mission introuvable")
    if body.role_id is not None:
        r = db.get(MissionRole, body.role_id)
        if not r or r.mission_id != mid:
            raise HTTPException(status_code=404, detail="Role introuvable")
    _assignment_inside_mission(m, body.start_at, body.end_at)
    if _overlap_exists(db, user_id=body.user_id, start_at=body.start_at, end_at=body.end_at):
        raise HTTPException(status_code=409, detail="Assignment overlap pour cet utilisateur")
    a = Assignment(
        mission_id=mid,
        role_id=body.role_id,
        user_id=body.user_id,
        start_at=body.start_at,
        end_at=body.end_at,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    write_audit(
        db,
        actor_user_id=user_id,
        action="assignment.create",
        entity="assignment",
        entity_id=str(a.id),
        details={"mission_id": mid},
    )
    return AssignmentOut.model_validate(a)


@router.delete("/{mid}/assignments/{aid}", status_code=204)
def delete_assignment(
    mid: int,
    aid: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    a = db.get(Assignment, aid)
    if not a or a.mission_id != mid:
        raise HTTPException(status_code=404, detail="Assignment introuvable")
    db.delete(a)
    db.commit()
    write_audit(
        db,
        actor_user_id=user_id,
        action="assignment.delete",
        entity="assignment",
        entity_id=str(aid),
        details={"mission_id": mid},
    )
    return None
