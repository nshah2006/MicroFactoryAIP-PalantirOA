def deterministic_recovery_plan(impact):
    actions = []
    if impact.available_substitutes:
        actions.append({
            "type": "approve_substitute",
            "label": f"Approve {impact.available_substitutes[0]} as substitute after QA validation",
            "requiresApproval": True,
            "approverRole": "Manufacturing Engineer",
        })
        actions.append({
            "type": "request_qa",
            "label": f"Create QA validation check for {impact.available_substitutes[0]}",
            "requiresApproval": False,
            "approverRole": None,
        })
    if impact.machines_with_available_capacity:
        actions.append({
            "type": "reschedule_machine",
            "label": f"Move {impact.blocked_work_orders[0]} to {impact.machines_with_available_capacity[0]} tonight",
            "requiresApproval": True,
            "approverRole": "Operations Manager",
        })
    if impact.delay_days > 2:
        actions.append({
            "type": "notify_supplier",
            "label": "Notify supplier and request expedited replacement batch",
            "requiresApproval": False,
            "approverRole": None,
        })
    return {
        "summary": f"{impact.affected_part_code} delay blocks {len(impact.blocked_work_orders)} work orders and puts {', '.join(impact.affected_builds)} at risk.",
        "riskLevel": impact.severity,
        "confidence": 82,
        "reasoningBullets": [
            f"{impact.affected_part_code} is required by {len(impact.blocked_work_orders)} active work orders.",
            "Substitute is available with high compatibility and requires QA validation.",
            "Available machine capacity can reduce delay impact.",
        ],
        "recommendedActions": actions,
    }
