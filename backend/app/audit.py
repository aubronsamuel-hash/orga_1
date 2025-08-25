import logging
from typing import Any

from sqlalchemy.orm import Session

from .models import AuditLog

log = logging.getLogger("audit")


def write_audit(
    db: Session,
    *,
    actor_user_id: int | None,
    action: str,
    entity: str,
    entity_id: str,
    details: dict[str, Any] | None = None,
) -> None:
    rec = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        entity=entity,
        entity_id=str(entity_id),
        details=details or {},
    )
    db.add(rec)
    db.commit()
    log.info("audit", extra={"action": action, "entity": entity, "entity_id": entity_id})
