from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.drone import Drone, DroneMission
from app.models.farm import Field

router = APIRouter()

class MissionCreate(BaseModel):
    drone_id: int
    field_id: int
    mission_type: str
    planned_start: Optional[datetime] = None
    altitude_m: float = 80.0
    overlap_percent: int = 70
    notes: Optional[str] = None

@router.get("/")
async def list_drones(farm_id: int = 1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Drone).where(Drone.farm_id == farm_id, Drone.is_active == True))
    drones = result.scalars().all()
    return [
        {"id": d.id, "name": d.name, "model": d.model, "serial_number": d.serial_number, "status": d.status,
         "battery_level": d.battery_level, "max_flight_time_min": d.max_flight_time_min, "camera_type": d.camera_type,
         "last_maintenance": d.last_maintenance.isoformat() if d.last_maintenance else None}
        for d in drones
    ]

@router.get("/{drone_id}")
async def get_drone(drone_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Drone).where(Drone.id == drone_id))
    drone = result.scalar_one_or_none()
    if not drone:
        raise HTTPException(status_code=404, detail="الطائرة غير موجودة")
    return {"id": drone.id, "name": drone.name, "model": drone.model, "status": drone.status,
            "battery_level": drone.battery_level, "camera_type": drone.camera_type, "max_flight_time_min": drone.max_flight_time_min}

@router.get("/missions/list")
async def list_missions(field_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(DroneMission).order_by(DroneMission.created_at.desc())
    if field_id:
        query = query.where(DroneMission.field_id == field_id)
    result = await db.execute(query.limit(20))
    missions = result.scalars().all()
    out = []
    for m in missions:
        drone_res = await db.execute(select(Drone).where(Drone.id == m.drone_id))
        drone = drone_res.scalar_one_or_none()
        field_res = await db.execute(select(Field).where(Field.id == m.field_id))
        field = field_res.scalar_one_or_none()
        out.append({
            "id": m.id, "drone_name": drone.name if drone else "—", "field_name": field.name if field else "—",
            "mission_type": m.mission_type, "status": m.status,
            "planned_start": m.planned_start.isoformat() if m.planned_start else None,
            "actual_start": m.actual_start.isoformat() if m.actual_start else None,
            "actual_end": m.actual_end.isoformat() if m.actual_end else None,
            "altitude_m": m.altitude_m, "area_covered_ha": m.area_covered_ha,
            "images_captured": m.images_captured, "notes": m.notes
        })
    return out

@router.post("/missions")
async def create_mission(mission: MissionCreate, db: AsyncSession = Depends(get_db)):
    drone_res = await db.execute(select(Drone).where(Drone.id == mission.drone_id))
    drone = drone_res.scalar_one_or_none()
    if not drone:
        raise HTTPException(status_code=404, detail="الطائرة غير موجودة")
    if drone.status not in ("idle", "charging"):
        raise HTTPException(status_code=400, detail=f"الطائرة غير متاحة (الحالة: {drone.status})")
    field_res = await db.execute(select(Field).where(Field.id == mission.field_id))
    field = field_res.scalar_one_or_none()
    if not field:
        raise HTTPException(status_code=404, detail="الحقل غير موجود")
    new_mission = DroneMission(
        drone_id=mission.drone_id, field_id=mission.field_id, mission_type=mission.mission_type,
        status="planned", planned_start=mission.planned_start or (datetime.utcnow() + timedelta(hours=1)),
        altitude_m=mission.altitude_m, overlap_percent=mission.overlap_percent, notes=mission.notes
    )
    db.add(new_mission)
    await db.flush()
    return {
        "message": "تم جدولة المهمة بنجاح", "mission_id": new_mission.id, "drone": drone.name,
        "field": field.name, "mission_type": mission.mission_type, "planned_start": new_mission.planned_start.isoformat()
    }

@router.post("/missions/{mission_id}/start")
async def start_mission(mission_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DroneMission).where(DroneMission.id == mission_id))
    mission = result.scalar_one_or_none()
    if not mission:
        raise HTTPException(status_code=404, detail="المهمة غير موجودة")
    if mission.status != "planned":
        raise HTTPException(status_code=400, detail="لا يمكن بدء هذه المهمة")
    mission.status = "in_progress"
    mission.actual_start = datetime.utcnow()
    drone_res = await db.execute(select(Drone).where(Drone.id == mission.drone_id))
    drone = drone_res.scalar_one()
    drone.status = "flying"
    return {"message": "بدأت المهمة", "mission_id": mission_id, "status": "in_progress"}

@router.post("/missions/{mission_id}/complete")
async def complete_mission(mission_id: int, images_count: int = 120, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DroneMission).where(DroneMission.id == mission_id))
    mission = result.scalar_one_or_none()
    if not mission:
        raise HTTPException(status_code=404, detail="المهمة غير موجودة")
    mission.status = "completed"
    mission.actual_end = datetime.utcnow()
    mission.images_captured = images_count
    field_res = await db.execute(select(Field).where(Field.id == mission.field_id))
    field = field_res.scalar_one_or_none()
    if field:
        mission.area_covered_ha = field.area_hectares
    drone_res = await db.execute(select(Drone).where(Drone.id == mission.drone_id))
    drone = drone_res.scalar_one()
    drone.status = "idle"
    drone.battery_level = max(20, drone.battery_level - 35)
    return {"message": "اكتملت المهمة بنجاح", "mission_id": mission_id, "images_captured": images_count, "area_covered_ha": mission.area_covered_ha}

@router.get("/stats")
async def drone_stats(farm_id: int = 1, db: AsyncSession = Depends(get_db)):
    drones_res = await db.execute(select(Drone).where(Drone.farm_id == farm_id))
    drones = drones_res.scalars().all()
    missions_res = await db.execute(select(DroneMission))
    missions = missions_res.scalars().all()
    completed = [m for m in missions if m.status == "completed"]
    return {
        "total_drones": len(drones),
        "available_drones": len([d for d in drones if d.status in ("idle", "charging")]),
        "flying_now": len([d for d in drones if d.status == "flying"]),
        "total_missions": len(missions),
        "completed_missions": len(completed),
        "total_images_captured": sum(m.images_captured for m in completed),
        "total_area_mapped_ha": round(sum(m.area_covered_ha or 0 for m in completed), 1)
    }
