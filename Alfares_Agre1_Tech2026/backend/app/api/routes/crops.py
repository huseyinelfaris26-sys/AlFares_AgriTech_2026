from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

router = APIRouter()

crops_db = [
    {"id": "crp-001", "name": "قمح شتوي", "scientific_name": "Triticum aestivum", "field_id": "fld-001",
     "planting_date": "2026-11-01", "expected_harvest": "2027-05-15", "growth_stage": "التفريع",
     "variety": "شام 8", "target_yield": 5.2, "current_status": "صحي"},
    {"id": "crp-002", "name": "ذرة صفراء", "scientific_name": "Zea mays", "field_id": "fld-002",
     "planting_date": "2026-04-10", "expected_harvest": "2026-09-20", "growth_stage": "النضج",
     "variety": "هجين محلي", "target_yield": 8.5, "current_status": "جيد"}
]

class CropPlan(BaseModel):
    name: str
    field_id: str
    planting_date: date
    variety: Optional[str] = None
    target_yield: Optional[float] = None

@router.get("/")
async def list_crops():
    return crops_db

@router.get("/{crop_id}")
async def get_crop(crop_id: str):
    for c in crops_db:
        if c["id"] == crop_id:
            return c
    raise HTTPException(status_code=404, detail="المحصول غير موجود")

@router.post("/plan")
async def create_crop_plan(plan: CropPlan):
    new_crop = {
        "id": f"crp-{len(crops_db)+1:03d}", "name": plan.name, "field_id": plan.field_id,
        "planting_date": plan.planting_date.isoformat(), "expected_harvest": None,
        "growth_stage": "البذر", "variety": plan.variety or "غير محدد",
        "target_yield": plan.target_yield, "current_status": "مخطط",
        "created_at": datetime.utcnow().isoformat()
    }
    crops_db.append(new_crop)
    return new_crop

@router.get("/calendar/{year}")
async def crop_calendar(year: int = 2026):
    return {
        "year": year, "region": "شمال سوريا / تل أبيض",
        "calendar": [
            {"month": 1, "activities": ["تحضير التربة", "صيانة المعدات"]},
            {"month": 2, "activities": ["تسميد أساسي", "فحص التربة"]},
            {"month": 3, "activities": ["زراعة محاصيل ربيعية مبكرة"]},
            {"month": 4, "activities": ["زراعة الذرة والقطن", "مكافحة الأعشاب"]},
            {"month": 5, "activities": ["ري وتسميد دقيق", "مراقبة الآفات"]},
            {"month": 6, "activities": ["حصاد القمح", "زراعة محاصيل صيفية"]},
            {"month": 7, "activities": ["ري مكثف", "مكافحة الحشرات"]},
            {"month": 8, "activities": ["حصاد الذرة المبكرة"]},
            {"month": 9, "activities": ["حصاد رئيسي", "تحضير للموسم الشتوي"]},
            {"month": 10, "activities": ["زراعة القمح والشعير"]},
            {"month": 11, "activities": ["تسميد شتوي", "مراقبة الطقس"]},
            {"month": 12, "activities": ["راحة التربة", "تحليل الموسم"]}
        ]
    }
