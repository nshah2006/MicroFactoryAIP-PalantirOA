import httpx

from app.core.config import settings
from app.schemas.recovery_plan import RecoveryPlan
from app.services.recommendation_engine import deterministic_recovery_plan

SYSTEM_PROMPT = "You are an operations recovery planner for a small manufacturing team. You must only use the operational context provided. Do not invent suppliers, parts, machines, work orders, or approvals. Return only valid JSON matching the provided schema. Critical actions require human approval. You are allowed to summarize risk and recommend next actions, but you are not allowed to directly approve or execute actions."


def generate_plan_with_fallback(impact):
    fallback = deterministic_recovery_plan(impact)
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{settings.ollama_base_url}/api/chat",
                json={
                    "model": settings.ollama_model,
                    "format": "json",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": str(fallback)},
                    ],
                    "stream": False,
                },
            )
            response.raise_for_status()
            payload = response.json()
            content = payload.get("message", {}).get("content", "")
            plan = RecoveryPlan.model_validate_json(content)
            return plan.model_dump()
    except Exception:
        fallback["aiStatus"] = "fallback_used"
        return RecoveryPlan(**fallback).model_dump()
