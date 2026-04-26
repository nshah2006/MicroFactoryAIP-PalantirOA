from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.action import Action
from app.models.issue import Issue
from app.services.agent_service import generate_plan_with_fallback
from app.services.audit_service import log_event
from app.services.impact_engine import analyze_supplier_delay

router = APIRouter(prefix="/recovery", tags=["recovery"])


class RecoveryRequest(BaseModel):
    issueCode: str


@router.post("/generate")
def generate(payload: RecoveryRequest, db: Session = Depends(get_db)):
    issue = db.query(Issue).filter(Issue.issue_code == payload.issueCode).first()
    impact = analyze_supplier_delay(db, issue.affected_part_code, 4)
    plan = generate_plan_with_fallback(impact)

    for i, action in enumerate(plan["recommendedActions"], start=22):
        db.add(Action(action_code=f"ACT-{i:03d}", issue_id=issue.id, type=action["type"], label=action["label"], requires_approval=action["requiresApproval"], approver_role=action["approverRole"], status="pending_approval" if action["requiresApproval"] else "recommended"))
    db.commit()
    log_event(db, "recovery.generated", "issue", issue.issue_code, "Recovery plan generated", actor="Local LLM", role="System")
    return plan
