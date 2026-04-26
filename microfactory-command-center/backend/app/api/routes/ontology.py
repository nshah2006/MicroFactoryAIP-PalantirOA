from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.ontology_service import build_graph

router = APIRouter(prefix="/ontology", tags=["ontology"])


@router.get("/graph")
def graph(db: Session = Depends(get_db)):
    return build_graph(db)
