from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    work_order_code: Mapped[str] = mapped_column(String(50), unique=True)
    build_id: Mapped[int] = mapped_column(ForeignKey("builds.id"))
    required_part_code: Mapped[str] = mapped_column(String(50))
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id"))
    owner_name: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(24), default="ready")
    blocker_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    due_at: Mapped[datetime] = mapped_column(DateTime)
    estimated_hours: Mapped[float] = mapped_column(Float, default=2.0)
    priority: Mapped[str] = mapped_column(String(24), default="medium")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
