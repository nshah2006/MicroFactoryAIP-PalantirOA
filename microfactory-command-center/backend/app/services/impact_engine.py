from dataclasses import dataclass

from sqlalchemy import select

from app.models.build import Build
from app.models.machine import Machine
from app.models.part import Part
from app.models.supplier import Supplier
from app.models.work_order import WorkOrder


@dataclass
class ImpactAnalysis:
    affected_part_code: str
    supplier_name: str
    delay_days: int
    blocked_work_orders: list[str]
    at_risk_work_orders: list[str]
    affected_builds: list[str]
    available_substitutes: list[str]
    machines_with_available_capacity: list[str]
    estimated_delay_days: int
    severity: str
    approval_required: bool


def _severity(blocked_count: int) -> str:
    if blocked_count > 10:
        return "critical"
    if 6 <= blocked_count <= 10:
        return "high"
    if 2 <= blocked_count <= 5:
        return "medium"
    return "low"


def analyze_supplier_delay(db, part_code: str, delay_days: int) -> ImpactAnalysis:
    part = db.scalar(select(Part).where(Part.part_code == part_code))
    supplier = db.scalar(select(Supplier).where(Supplier.id == part.supplier_id))
    work_orders = db.scalars(select(WorkOrder).where(WorkOrder.required_part_code == part_code)).all()

    blocked = [wo.work_order_code for wo in work_orders]
    build_ids = sorted({wo.build_id for wo in work_orders})
    builds = db.scalars(select(Build).where(Build.id.in_(build_ids))).all() if build_ids else []

    machines = db.scalars(select(Machine).where(Machine.status == "available")).all()
    available_substitutes = [part.substitute_part_code] if part.substitute_part_code else []

    return ImpactAnalysis(
        affected_part_code=part_code,
        supplier_name=supplier.name,
        delay_days=delay_days,
        blocked_work_orders=blocked,
        at_risk_work_orders=[],
        affected_builds=[b.build_code for b in builds],
        available_substitutes=available_substitutes,
        machines_with_available_capacity=[m.machine_code for m in machines],
        estimated_delay_days=delay_days,
        severity=_severity(len(blocked)),
        approval_required=True,
    )
