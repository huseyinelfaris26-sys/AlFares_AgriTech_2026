from sqlalchemy import String, Float, Integer, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from app.core.database import Base

class Crop(Base):
    __tablename__ = "crops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    scientific_name: Mapped[str | None] = mapped_column(String(150))
    variety: Mapped[str | None] = mapped_column(String(100))
    planting_date: Mapped[date | None] = mapped_column(Date)
    expected_harvest: Mapped[date | None] = mapped_column(Date)
    growth_stage: Mapped[str] = mapped_column(String(50), default="بذر")
    target_yield: Mapped[float | None] = mapped_column(Float)
    current_status: Mapped[str] = mapped_column(String(50), default="صحي")
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    field = relationship("Field", back_populates="crops")

class CropPlan(Base):
    __tablename__ = "crop_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    farm_id: Mapped[int] = mapped_column(Integer, ForeignKey("farms.id"))
    year: Mapped[int] = mapped_column(Integer)
    season: Mapped[str] = mapped_column(String(50))
    crop_name: Mapped[str] = mapped_column(String(100))
    planned_area_hectares: Mapped[float] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
