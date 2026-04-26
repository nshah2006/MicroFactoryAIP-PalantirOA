from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.seed_service import reset_seed

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("/reset")
def reset(db: Session = Depends(get_db)):
    reset_seed(db)
    return {"status": "ok"}
