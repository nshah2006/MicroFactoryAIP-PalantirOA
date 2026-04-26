from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.build import Build
from app.models.issue import Issue
from app.models.part import Part
from app.models.supplier import Supplier
from app.models.work_order import WorkOrder
from app.services.audit_service import log_event
from app.services.impact_engine import analyze_supplier_delay

router = APIRouter(prefix="/disruptions", tags=["disruptions"])


class DelayRequest(BaseModel):
    supplierName: str
    partCode: str
    delayDays: int


@router.post("/supplier-delay")
def supplier_delay(payload: DelayRequest, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.name == payload.supplierName).first()
    part = db.query(Part).filter(Part.part_code == payload.partCode).first()

    supplier.status = "delayed"
    supplier.current_delay_days = payload.delayDays
    part.status = "shortage"

    impact = analyze_supplier_delay(db, payload.partCode, payload.delayDays)
    blocked = db.query(WorkOrder).filter(WorkOrder.required_part_code == payload.partCode).all()
    for wo in blocked:
        wo.status = "blocked"
        wo.blocker_reason = f"Supplier delay on {payload.partCode}"

    build_ids = sorted({wo.build_id for wo in blocked})
    for build in db.query(Build).filter(Build.id.in_(build_ids)).all():
        build.status = "at_risk"

    issue = Issue(issue_code="ISS-009", type="supplier_delay", severity=impact.severity, title=f"Supplier delay for {payload.partCode}", description=f"{payload.supplierName} delayed by {payload.delayDays} days", affected_part_code=payload.partCode, affected_supplier_id=supplier.id, status="open")
    db.add(issue)
    db.commit()

    log_event(db, "disruption.detected", "issue", "ISS-009", f"Supplier delay detected for {payload.partCode}")
    log_event(db, "impact.analyzed", "issue", "ISS-009", f"{len(impact.blocked_work_orders)} blocked work orders identified", actor="Impact Engine", role="System")

    return {
        "issueCode": "ISS-009",
        "affectedPart": payload.partCode,
        "blockedWorkOrders": impact.blocked_work_orders,
        "affectedBuilds": impact.affected_builds,
        "estimatedDelayDays": payload.delayDays,
        "substitutePart": "DRV-042B",
        "approvalRequired": True,
    }
