from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class QualityCheck(Base):
    __tablename__ = "quality_checks"

    id: Mapped[int] = mapped_column(primary_key=True)
    check_code: Mapped[str] = mapped_column(String(50), unique=True)
    work_order_id: Mapped[int] = mapped_column(ForeignKey("work_orders.id"))
    part_code: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(24), default="pending")
    defect_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    qa_owner: Mapped[str] = mapped_column(String(80), default="QA Team")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
