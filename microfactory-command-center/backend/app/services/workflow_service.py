from sqlalchemy import select

from app.models.action import Action
from app.models.quality_check import QualityCheck
from app.models.work_order import WorkOrder
from app.services.audit_service import log_event


def approve_action(db, action_code: str, actor: str, role: str):
    action = db.scalar(select(Action).where(Action.action_code == action_code))
    if not action:
        raise ValueError("Action not found")
    if action.requires_approval and action.approver_role and action.approver_role != role:
        raise PermissionError(f"Approval blocked: this action requires {action.approver_role} permissions.")

    action.status = "approved"
    action.approved_by = actor
    db.add(action)

    if action.type == "approve_substitute":
        blocked = db.scalars(select(WorkOrder).where(WorkOrder.status == "blocked")).all()
        for wo in blocked:
            wo.status = "at_risk"
            wo.blocker_reason = "Awaiting QA validation for substitute"
            db.add(wo)
        qc = QualityCheck(check_code="QC-900", work_order_id=blocked[0].id, part_code="DRV-042B", status="pending", qa_owner="QA Team")
        db.add(qc)

    db.commit()
    return log_event(db, "action.approved", "action", action.action_code, f"{actor} approved {action.label}", actor=actor, role=role)
