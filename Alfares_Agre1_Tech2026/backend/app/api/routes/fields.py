from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter()

fields_db = [
    {"id": "fld-001", "name": "الحقل الشمالي", "area_hectares": 12.5, "crop_type": "قمح", "soil_type": "طيني لومي",
     "location": {"lat": 36.52, "lng": 37.15}, "status": "active", "health_score": 91, "last_irrigation": "2026-11-15T08:00:00", "sensors_count": 8},
    {"id": "fld-002", "name": "الحقل الجنوبي", "area_hectares": 8.3, "crop_type": "ذرة", "soil_type": "رملي طيني",
     "location": {"lat": 36.51, "lng": 37.16}, "status": "active", "health_score": 78, "last_irrigation": "2026-11-16T06:30:00", "sensors_count": 5},
    {"id": "fld-003", "name": "الحقل الشرقي", "area_hectares": 15.0, "crop_type": "قطن", "soil_type": "طيني",
     "location": {"lat": 36.525, "lng": 37.17}, "status": "active", "health_score": 85, "last_irrigation": "2026-11-14T19:00:00", "sensors_count": 10}
]

class FieldCreate(BaseModel):
    name: str
    area_hectares: float
    crop_type: str
    soil_type: Optional[str] = None
    location: Optional[dict] = None

class FieldUpdate(BaseModel):
    name: Optional[str] = None
    area_hectares: Optional[float] = None
    crop_type: Optional[str] = None
    soil_type: Optional[str] = None
    status: Optional[str] = None

@router.get("/", response_model=List[dict])
async def list_fields():
    return fields_db

@router.get("/{field_id}")
async def get_field(field_id: str):
    for f in fields_db:
        if f["id"] == field_id:
            return f
    raise HTTPException(status_code=404, detail="الحقل غير موجود")

@router.post("/")
async def create_field(field: FieldCreate):
    new_field = {
        "id": f"fld-{str(uuid.uuid4())[:8]}", "name": field.name, "area_hectares": field.area_hectares,
        "crop_type": field.crop_type, "soil_type": field.soil_type or "غير محدد",
        "location": field.location or {"lat": 0, "lng": 0}, "status": "active", "health_score": 80,
        "last_irrigation": None, "sensors_count": 0, "created_at": datetime.utcnow().isoformat()
    }
    fields_db.append(new_field)
    return new_field

@router.put("/{field_id}")
async def update_field(field_id: str, update: FieldUpdate):
    for i, f in enumerate(fields_db):
        if f["id"] == field_id:
            data = update.dict(exclude_unset=True)
            fields_db[i].update(data)
            return fields_db[i]
    raise HTTPException(status_code=404, detail="الحقل غير موجود")

@router.delete("/{field_id}")
async def delete_field(field_id: str):
    global fields_db
    fields_db = [f for f in fields_db if f["id"] != field_id]
    return {"message": "تم حذف الحقل بنجاح"}
