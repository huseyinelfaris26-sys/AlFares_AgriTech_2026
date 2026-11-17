from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter()

class IrrigationSchedule(BaseModel):
    field_id: str
    start_time: datetime
    duration_minutes: int
    water_amount_mm: float
    method: str = "drip"

class FertilizationPlan(BaseModel):
    field_id: str
    nutrient: str
    amount_kg_ha: float
    application_date: datetime
    method: str = "variable_rate"

@router.get("/status/{field_id}")
async def irrigation_status(field_id: str):
    return {
        "field_id": field_id,
        "soil_moisture": round(random.uniform(25, 55), 1),
        "optimal_range": [30, 50],
        "last_irrigation": "2026-11-16T06:30:00",
        "next_recommended": "2026-11-18T07:00:00",
        "water_used_this_week_mm": 28.5,
        "efficiency_score": 91.2,
        "sensors": [
            {"id": "sm-01", "depth_cm": 15, "moisture": 42.3},
            {"id": "sm-02", "depth_cm": 30, "moisture": 38.7},
            {"id": "sm-03", "depth_cm": 45, "moisture": 35.1}
        ]
    }

@router.post("/schedule")
async def create_irrigation_schedule(schedule: IrrigationSchedule):
    return {
        "message": "تم جدولة الري بنجاح",
        "schedule_id": f"irr-{datetime.utcnow().strftime('%Y%m%d%H%M')}",
        "details": schedule.dict(),
        "estimated_water_m3": round(schedule.water_amount_mm * 10, 2)
    }

@router.post("/fertilization")
async def create_fertilization_plan(plan: FertilizationPlan):
    return {
        "message": "تم إنشاء خطة التسميد الدقيق",
        "plan_id": f"fert-{datetime.utcnow().strftime('%Y%m%d%H%M')}",
        "prescription": {
            "type": "variable_rate", "nutrient": plan.nutrient, "rate_kg_ha": plan.amount_kg_ha,
            "zones": [{"zone": "A", "rate_factor": 0.85}, {"zone": "B", "rate_factor": 1.0}, {"zone": "C", "rate_factor": 1.15}]
        },
        "details": plan.dict()
    }

@router.get("/recommendations/{field_id}")
async def get_recommendations(field_id: str):
    return {
        "field_id": field_id,
        "irrigation": {"action": "ري خفيف", "amount_mm": 12, "reason": "رطوبة التربة تقترب من الحد الأدنى"},
        "fertilization": {"action": "إضافة نيتروجين", "amount_kg_ha": 25, "timing": "خلال 3 أيام", "reason": "مرحلة النمو النشط تحتاج دعم نيتروجيني"}
    }
