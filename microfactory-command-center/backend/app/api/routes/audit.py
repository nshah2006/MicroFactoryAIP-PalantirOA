from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.audit_event import AuditEvent

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("")
def list_audit(limit: int = 50, db: Session = Depends(get_db)):
    events = db.query(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(limit).all()
    return [{"time": e.created_at.isoformat(), "actor": e.actor, "role": e.role, "entity": e.entity_type, "message": e.message} for e in events]
