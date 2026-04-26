from pydantic import BaseModel


class RecommendedAction(BaseModel):
    type: str
    label: str
    requiresApproval: bool
    approverRole: str | None = None


class RecoveryPlan(BaseModel):
    summary: str
    riskLevel: str
    confidence: int
    reasoningBullets: list[str]
    recommendedActions: list[RecommendedAction]
    aiStatus: str = "ok"
