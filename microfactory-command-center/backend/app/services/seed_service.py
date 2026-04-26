from datetime import datetime, timedelta

from sqlalchemy import delete

from app.models.action import Action
from app.models.audit_event import AuditEvent
from app.models.build import Build
from app.models.issue import Issue
from app.models.machine import Machine
from app.models.part import Part
from app.models.quality_check import QualityCheck
from app.models.supplier import Supplier
from app.models.work_order import WorkOrder


def reset_seed(db):
    for model in [Action, AuditEvent, QualityCheck, Issue, WorkOrder, Part, Machine, Build, Supplier]:
        db.execute(delete(model))
    db.commit()

    suppliers = [
        Supplier(name="Northline Components", reliability_score=74, average_delay_days=2, status="normal", contact_email="northline@example.com"),
        Supplier(name="Apex Motion Supply", reliability_score=88, average_delay_days=1, status="normal", contact_email="apex@example.com"),
        Supplier(name="Vertex Electronics", reliability_score=85, average_delay_days=1, status="normal", contact_email="vertex@example.com"),
        Supplier(name="BlueForge Metals", reliability_score=91, average_delay_days=0, status="normal", contact_email="blueforge@example.com"),
        Supplier(name="Orion Industrial Systems", reliability_score=80, average_delay_days=2, status="normal", contact_email="orion@example.com"),
    ]
    db.add_all(suppliers)
    db.commit()
    names = {s.name: s.id for s in db.query(Supplier).all()}

    parts = [
        ("DRV-042", "Motor Driver Board", "controls", 10, 35, "DRV-042B", 0.91, "Northline Components"),
        ("DRV-042B", "Motor Driver Board Substitute", "controls", 16, 5, None, None, "Apex Motion Supply"),
        ("SNS-118", "Optical Sensor", "sensing", 42, 20, None, None, "Vertex Electronics"),
        ("BRK-201", "Aluminum Bracket", "frame", 90, 40, None, None, "BlueForge Metals"),
        ("PWR-090", "Power Regulator", "power", 18, 15, None, None, "Apex Motion Supply"),
        ("CBL-014", "Shielded Cable", "wiring", 220, 150, None, None, "Orion Industrial Systems"),
        ("MNT-300", "Mounting Plate", "frame", 65, 33, None, None, "BlueForge Metals"),
        ("FAN-022", "Cooling Fan", "thermal", 30, 22, None, None, "Orion Industrial Systems"),
        ("PCB-700", "Control PCB", "controls", 21, 18, None, None, "Vertex Electronics"),
        ("ENC-044", "Enclosure", "frame", 54, 30, None, None, "BlueForge Metals"),
        ("BOLT-006", "M6 Bolt Kit", "hardware", 400, 180, None, None, "BlueForge Metals"),
        ("QA-JIG-03", "Test Jig", "qa", 7, 6, None, None, "Apex Motion Supply"),
    ]
    for code, name, cat, qoh, req, sub, score, supplier in parts:
        db.add(Part(part_code=code, name=name, category=cat, quantity_on_hand=qoh, quantity_required=req, reorder_threshold=12, lead_time_days=4, supplier_id=names[supplier], substitute_part_code=sub, compatibility_score=score, status="available"))

    machines = [
        Machine(machine_code="CNC-1", name="CNC Cell 1", capability="Milling", status="available", available_window="19:00-22:00"),
        Machine(machine_code="CNC-2", name="CNC Cell 2", capability="Milling", status="available", available_window="20:00-23:00"),
        Machine(machine_code="ASM-1", name="Assembly Line 1", capability="Assembly", status="busy", available_window="23:00-01:00"),
        Machine(machine_code="QA-BENCH-2", name="QA Bench", capability="Validation", status="available", available_window="18:00-20:00"),
        Machine(machine_code="PRINT-3D-4", name="3D Printer", capability="Rapid part", status="maintenance", available_window="N/A"),
    ]
    db.add_all(machines)

    now = datetime.utcnow()
    builds = [
        Build(build_code="BUILD-A", name="Autonomous Drone Assembly", customer="AeroNorth", shipment_due_at=now+timedelta(days=4), status="on_track", priority="high"),
        Build(build_code="BUILD-B", name="Sensor Rig Prototype", customer="Delta Lab", shipment_due_at=now+timedelta(days=5), status="on_track", priority="high"),
        Build(build_code="BUILD-C", name="Inspection Robot Batch", customer="MetroFab", shipment_due_at=now+timedelta(days=6), status="on_track", priority="medium"),
    ]
    db.add_all(builds)
    db.commit()

    builds_by = {b.build_code: b.id for b in db.query(Build).all()}
    machines_by = {m.machine_code: m.id for m in db.query(Machine).all()}

    wo_codes = ["WO-018","WO-021","WO-024","WO-026","WO-031","WO-033","WO-037"]
    for i in range(1,16):
        code = f"WO-{i:03d}" if i<10 else f"WO-{i:03d}"
        code = wo_codes[i-1] if i<=7 else code
        req = "DRV-042" if i<=7 else "SNS-118"
        build = ["BUILD-A","BUILD-B","BUILD-C"][i%3]
        machine = ["CNC-1","CNC-2","ASM-1","QA-BENCH-2","PRINT-3D-4"][i%5]
        db.add(WorkOrder(work_order_code=code, build_id=builds_by[build], required_part_code=req, machine_id=machines_by[machine], owner_name="Ops Team", status="ready", due_at=now+timedelta(days=(i%4)+1), estimated_hours=2.5, priority="high" if i<=7 else "medium"))

    db.add(AuditEvent(event_type="system.seeded", entity_type="system", entity_id="seed", actor="System", role="System", message="Seed reset completed"))
    db.commit()
