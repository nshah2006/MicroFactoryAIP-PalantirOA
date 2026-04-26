from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.work_order import WorkOrder

router = APIRouter(prefix="/work-orders", tags=["work-orders"])


@router.get("")
def list_work_orders(status: str | None = None, build_code: str | None = None, part_code: str | None = None, priority: str | None = None, db: Session = Depends(get_db)):
    query = db.query(WorkOrder)
    if status:
        query = query.filter(WorkOrder.status == status)
    if part_code:
        query = query.filter(WorkOrder.required_part_code == part_code)
    if priority:
        query = query.filter(WorkOrder.priority == priority)
    records = query.all()
    return [{"work_order_code": r.work_order_code, "build_id": r.build_id, "required_part_code": r.required_part_code, "machine_id": r.machine_id, "owner_name": r.owner_name, "status": r.status, "blocker_reason": r.blocker_reason, "due_at": r.due_at.isoformat(), "estimated_hours": r.estimated_hours, "priority": r.priority} for r in records]


@router.get("/{work_order_code}")
def get_work_order(work_order_code: str, db: Session = Depends(get_db)):
    record = db.query(WorkOrder).filter(WorkOrder.work_order_code == work_order_code).first()
    return record
