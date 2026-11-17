from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class Drone(Base):
    __tablename__ = "drones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    farm_id: Mapped[int] = mapped_column(Integer, ForeignKey("farms.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100))
    serial_number: Mapped[str | None] = mapped_column(String(100), unique=True)
    status: Mapped[str] = mapped_column(String(30), default="idle")
    battery_level: Mapped[int] = mapped_column(Integer, default=100)
    max_flight_time_min: Mapped[int] = mapped_column(Integer, default=40)
    camera_type: Mapped[str] = mapped_column(String(50), default="RGB")
    last_maintenance: Mapped[datetime | None] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    farm = relationship("Farm", back_populates="drones")
    missions = relationship("DroneMission", back_populates="drone", cascade="all, delete-orphan")

class DroneMission(Base):
    __tablename__ = "drone_missions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drone_id: Mapped[int] = mapped_column(Integer, ForeignKey("drones.id"), nullable=False)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.id"), nullable=False)
    mission_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(30), default="planned")
    planned_start: Mapped[datetime | None] = mapped_column(DateTime)
    actual_start: Mapped[datetime | None] = mapped_column(DateTime)
    actual_end: Mapped[datetime | None] = mapped_column(DateTime)
    altitude_m: Mapped[float] = mapped_column(Float, default=80.0)
    overlap_percent: Mapped[int] = mapped_column(Integer, default=70)
    flight_path: Mapped[dict | None] = mapped_column(JSON)
    area_covered_ha: Mapped[float | None] = mapped_column(Float)
    images_captured: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    drone = relationship("Drone", back_populates="missions")
    field = relationship("Field", back_populates="drone_missions")
    images = relationship("DroneImage", back_populates="mission", cascade="all, delete-orphan")

class DroneImage(Base):
    __tablename__ = "drone_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_id: Mapped[int] = mapped_column(Integer, ForeignKey("drone_missions.id"), nullable=False)
    file_url: Mapped[str] = mapped_column(String(500))
    thumbnail_url: Mapped[str | None] = mapped_column(String(500))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    altitude_m: Mapped[float | None] = mapped_column(Float)
    capture_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    image_type: Mapped[str] = mapped_column(String(30), default="RGB")
    ai_analyzed: Mapped[bool] = mapped_column(Boolean, default=False)
    health_score: Mapped[float | None] = mapped_column(Float)
    detected_issues: Mapped[dict | None] = mapped_column(JSON)

    mission = relationship("DroneMission", back_populates="images")
