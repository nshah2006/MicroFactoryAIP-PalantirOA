from app.schemas.recovery_plan import RecoveryPlan


def test_schema_valid():
    payload = {
        "summary": "ok",
        "riskLevel": "high",
        "confidence": 90,
        "reasoningBullets": ["a"],
        "recommendedActions": [{"type": "approve_substitute", "label": "x", "requiresApproval": True, "approverRole": "Manufacturing Engineer"}],
    }
    assert RecoveryPlan(**payload)
