from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...deps import get_current_user_id, get_db
from ...models import Assignment, Availability

router = APIRouter(prefix="/conflicts", tags=["conflicts"])


def _now_utc() -> datetime:
    return datetime.now(UTC)


@router.get("", response_model=list[dict[str, Any]])
def list_conflicts(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    since: datetime | None = Query(None),
    until: datetime | None = Query(None),
) -> list[dict]:
    """
    Conflit = assignment [a_start,a_end] non integralement couvert par une availability [s,e] du user.
    """
    now = _now_utc()
    start = since or now - timedelta(days=1)
    end = until or now + timedelta(days=90)

    assigns = db.scalars(
        select(Assignment).where(
            Assignment.user_id == user_id,
            Assignment.start_at < end,
            Assignment.end_at > start,
        )
    ).all()

    avs = db.scalars(
        select(Availability).where(
            Availability.user_id == user_id,
            Availability.start_at < end,
            Availability.end_at > start,
        )
    ).all()

    conflicts: list[dict] = []
    for a in assigns:
        covered = any(av.start_at <= a.start_at and av.end_at >= a.end_at for av in avs)
        if not covered:
            conflicts.append(
                {
                    "assignment_id": a.id,
                    "mission_id": a.mission_id,
                    "start_at": a.start_at.isoformat(),
                    "end_at": a.end_at.isoformat(),
                    "reason": "not_covered",
                }
            )
    return conflicts

