from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import actions, audit, dashboard, disruptions, health, ontology, recovery, seed, work_orders
from app.core.config import settings
from app.core.database import Base, engine

app = FastAPI(title="MicroFactory Command Center Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[s.strip() for s in settings.backend_cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(health.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(ontology.router, prefix="/api")
app.include_router(work_orders.router, prefix="/api")
app.include_router(disruptions.router, prefix="/api")
app.include_router(recovery.router, prefix="/api")
app.include_router(actions.router, prefix="/api")
app.include_router(audit.router, prefix="/api")
app.include_router(seed.router, prefix="/api")
