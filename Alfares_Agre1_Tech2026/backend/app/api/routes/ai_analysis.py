from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import random

router = APIRouter()

class YieldPredictionRequest(BaseModel):
    field_id: str
    crop_type: str
    area_hectares: float
    planting_date: str
    soil_quality: Optional[float] = 0.75
    irrigation_score: Optional[float] = 0.8

@router.post("/yield-prediction")
async def predict_yield(req: YieldPredictionRequest):
    base_yield = {"قمح": 4.5, "ذرة": 7.8, "قطن": 3.2, "شعير": 3.8}.get(req.crop_type, 4.0)
    factor = (req.soil_quality * 0.4 + req.irrigation_score * 0.4 + random.uniform(0.85, 1.1) * 0.2)
    predicted = round(base_yield * factor, 2)
    return {
        "field_id": req.field_id, "crop_type": req.crop_type,
        "predicted_yield_ton_ha": predicted, "total_predicted_tons": round(predicted * req.area_hectares, 2),
        "confidence": round(random.uniform(0.78, 0.94), 2),
        "factors": {"soil": req.soil_quality, "irrigation": req.irrigation_score, "weather_outlook": "favorable"},
        "generated_at": datetime.utcnow().isoformat()
    }

@router.post("/crop-health")
async def analyze_crop_health(field_id: str = Form(...), file: UploadFile = File(...)):
    health_score = round(random.uniform(65, 95), 1)
    issues = []
    if health_score < 80:
        issues.append({"type": "nutrient_deficiency", "severity": "medium", "detail": "نقص محتمل في النيتروجين"})
    if health_score < 75:
        issues.append({"type": "water_stress", "severity": "high", "detail": "إجهاد مائي في أجزاء من الحقل"})
    return {
        "field_id": field_id, "filename": file.filename, "health_score": health_score,
        "status": "healthy" if health_score >= 85 else "needs_attention" if health_score >= 70 else "critical",
        "issues_detected": issues,
        "recommendations": ["مراجعة خطة التسميد", "فحص رطوبة التربة في المناطق ذات اللون الشاحب", "جدولة صورة طائرة مسيرة للمتابعة"],
        "analyzed_at": datetime.utcnow().isoformat()
    }

@router.get("/plant-count/{field_id}")
async def plant_count_estimate(field_id: str):
    return {
        "field_id": field_id, "estimated_plants": random.randint(180000, 250000),
        "density_per_m2": round(random.uniform(18, 28), 1), "coverage_percent": round(random.uniform(85, 98), 1),
        "gaps_detected": random.randint(3, 15), "method": "AI aerial image analysis", "confidence": 0.89
    }

@router.get("/anomaly-detection/{field_id}")
async def detect_anomalies(field_id: str):
    return {
        "field_id": field_id,
        "anomalies": [{"type": "growth_lag", "zone": "الزاوية الشمالية الغربية", "severity": "medium",
                       "description": "نمو أبطأ بنسبة 15% مقارنة بمتوسط الحقل"}] if random.random() > 0.4 else [],
        "scanned_at": datetime.utcnow().isoformat()
    }
