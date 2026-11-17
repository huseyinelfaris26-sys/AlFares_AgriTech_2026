from sqlalchemy import String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class SatelliteImage(Base):
    __tablename__ = "satellite_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id"), nullable=False)
    source: Mapped[str] = mapped_column(String(50))
    image_type: Mapped[str] = mapped_column(String(50))
    capture_date: Mapped[datetime] = mapped_column(DateTime)
    resolution_m: Mapped[float] = mapped_column(Float, default=10.0)
    cloud_cover: Mapped[float] = mapped_column(Float, default=0.0)
    file_url: Mapped[str | None] = mapped_column(String(500))
    ndvi_mean: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    field = relationship("Field", back_populates="satellite_images")

class NDVIRecord(Base):
    __tablename__ = "ndvi_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime)
    ndvi_mean: Mapped[float] = mapped_column(Float)
    ndvi_min: Mapped[float | None] = mapped_column(Float)
    ndvi_max: Mapped[float | None] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(50), default="Sentinel-2")
