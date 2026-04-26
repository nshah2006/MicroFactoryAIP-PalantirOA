from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.action import Action
from app.services.workflow_service import approve_action

router = APIRouter(prefix="/actions", tags=["actions"])


class ApproveRequest(BaseModel):
    actor: str
    role: str


class RejectRequest(ApproveRequest):
    reason: str


@router.post("/{action_code}/approve")
def approve(action_code: str, payload: ApproveRequest, db: Session = Depends(get_db)):
    try:
        event = approve_action(db, action_code, payload.actor, payload.role)
        return {"status": "approved", "event": event.message}
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@router.post("/{action_code}/reject")
def reject(action_code: str, payload: RejectRequest, db: Session = Depends(get_db)):
    action = db.query(Action).filter(Action.action_code == action_code).first()
    action.status = "rejected"
    db.add(action)
    db.commit()
    return {"status": "rejected", "reason": payload.reason}
