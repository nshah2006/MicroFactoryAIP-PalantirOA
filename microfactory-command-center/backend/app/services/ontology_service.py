from sqlalchemy import select

from app.models.build import Build
from app.models.machine import Machine
from app.models.part import Part
from app.models.supplier import Supplier
from app.models.work_order import WorkOrder


def build_graph(db):
    nodes = []
    edges = []
    suppliers = db.scalars(select(Supplier)).all()
    parts = db.scalars(select(Part)).all()
    work_orders = db.scalars(select(WorkOrder)).all()
    machines = db.scalars(select(Machine)).all()
    builds = db.scalars(select(Build)).all()

    for s in suppliers:
        nodes.append({"id": f"supplier-{s.id}", "type": "supplier", "label": s.name, "status": s.status, "metadata": {}})
    for p in parts:
        nodes.append({"id": f"part-{p.part_code.lower()}", "type": "part", "label": p.part_code, "status": p.status, "metadata": {}})
        edges.append({"id": f"edge-s-p-{p.id}", "source": f"supplier-{p.supplier_id}", "target": f"part-{p.part_code.lower()}", "label": "supplies"})
    for wo in work_orders:
        nodes.append({"id": f"wo-{wo.work_order_code.lower()}", "type": "work_order", "label": wo.work_order_code, "status": wo.status, "metadata": {}})
        edges.append({"id": f"edge-p-wo-{wo.id}", "source": f"part-{wo.required_part_code.lower()}", "target": f"wo-{wo.work_order_code.lower()}", "label": "required_by"})
        edges.append({"id": f"edge-wo-m-{wo.id}", "source": f"wo-{wo.work_order_code.lower()}", "target": f"machine-{wo.machine_id}", "label": "scheduled_on"})
        edges.append({"id": f"edge-wo-b-{wo.id}", "source": f"wo-{wo.work_order_code.lower()}", "target": f"build-{wo.build_id}", "label": "contributes_to"})
    for m in machines:
        nodes.append({"id": f"machine-{m.id}", "type": "machine", "label": m.machine_code, "status": m.status, "metadata": {}})
    for b in builds:
        nodes.append({"id": f"build-{b.id}", "type": "build", "label": b.build_code, "status": b.status, "metadata": {}})

    return {"nodes": nodes, "edges": edges}
