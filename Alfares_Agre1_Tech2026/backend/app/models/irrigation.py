from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class IrrigationRecord(Base):
    __tablename__ = "irrigation_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    water_amount_mm: Mapped[float] = mapped_column(Float)
    method: Mapped[str] = mapped_column(String(30), default="drip")
    status: Mapped[str] = mapped_column(String(30), default="scheduled")
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    field = relationship("Field", back_populates="irrigation_records")

class FertilizationRecord(Base):
    __tablename__ = "fertilization_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id"), nullable=False)
    nutrient: Mapped[str] = mapped_column(String(50))
    amount_kg_ha: Mapped[float] = mapped_column(Float)
    application_date: Mapped[datetime] = mapped_column(DateTime)
    method: Mapped[str] = mapped_column(String(50), default="variable_rate")
    prescription_zones: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="planned")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
