from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Part(Base):
    __tablename__ = "parts"

    id: Mapped[int] = mapped_column(primary_key=True)
    part_code: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(80), default="general")
    quantity_on_hand: Mapped[int] = mapped_column(Integer, default=0)
    quantity_required: Mapped[int] = mapped_column(Integer, default=0)
    reorder_threshold: Mapped[int] = mapped_column(Integer, default=0)
    lead_time_days: Mapped[int] = mapped_column(Integer, default=1)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    substitute_part_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    compatibility_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="available")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
