from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.build import Build
from app.models.issue import Issue
from app.models.work_order import WorkOrder

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return {
        "activeIssues": db.query(Issue).filter(Issue.status == "open").count(),
        "blockedWorkOrders": db.query(WorkOrder).filter(WorkOrder.status == "blocked").count(),
        "atRiskBuilds": db.query(Build).filter(Build.status == "at_risk").count(),
        "estimatedDelayDays": 4,
        "manualAnalysisMinutesSaved": 30,
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
    }
