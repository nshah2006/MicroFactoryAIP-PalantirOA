from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    reliability_score: Mapped[int] = mapped_column(Integer, default=85)
    average_delay_days: Mapped[int] = mapped_column(Integer, default=0)
    current_delay_days: Mapped[int] = mapped_column(Integer, default=0)
    contact_email: Mapped[str] = mapped_column(String(255), default="ops@example.com")
    status: Mapped[str] = mapped_column(String(24), default="normal")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
