from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import random

router = APIRouter()

class PestAlert(BaseModel):
    field_id: str
    pest_name: str
    severity: str
    confidence: float
    location: Optional[dict] = None
    notes: Optional[str] = None

@router.get("/alerts")
async def list_alerts():
    return [
        {"id": "pst-001", "field_id": "fld-002", "pest_name": "من القمح (Aphids)", "severity": "medium",
         "confidence": 0.87, "detected_at": "2026-11-17T14:20:00", "status": "active",
         "recommended_action": "رش مبيد حشري انتقائي + مراقبة"},
        {"id": "pst-002", "field_id": "fld-003", "pest_name": "دودة اللوز الشوكية", "severity": "low",
         "confidence": 0.72, "detected_at": "2026-11-16T09:15:00", "status": "monitoring",
         "recommended_action": "مراقبة أسبوعية"}
    ]

@router.post("/detect")
async def detect_pest(alert: PestAlert):
    return {"message": "تم تسجيل تنبيه الآفة", "alert_id": f"pst-{datetime.utcnow().strftime('%H%M%S')}",
            "status": "queued_for_analysis", **alert.dict()}

@router.post("/analyze-image")
async def analyze_pest_image(file: UploadFile = File(...)):
    possible_pests = [
        {"name": "منّ القطن", "confidence": 0.91, "severity": "high"},
        {"name": "صدأ الأوراق", "confidence": 0.78, "severity": "medium"},
        {"name": "لا توجد آفات واضحة", "confidence": 0.95, "severity": "none"}
    ]
    result = random.choice(possible_pests)
    return {
        "filename": file.filename, "analysis_time": datetime.utcnow().isoformat(),
        "detection": result,
        "recommendations": ["التقاط صور إضافية من زوايا مختلفة", "مقارنة مع صور سابقة لنفس الحقل", "استشارة مهندس زراعي إذا كانت الثقة > 80%"]
    }

@router.get("/common-pests")
async def common_pests_region():
    return {
        "region": "شمال سوريا", "season": "خريف/شتاء 2026",
        "common": [
            {"name": "من القمح", "crops": ["قمح", "شعير"], "peak_months": [3, 4, 5]},
            {"name": "صدأ الساق", "crops": ["قمح"], "peak_months": [4, 5]},
            {"name": "دودة ثمار التفاح", "crops": ["تفاح", "إجاص"], "peak_months": [6, 7, 8]},
            {"name": "الذبابة البيضاء", "crops": ["قطن", "خضروات"], "peak_months": [7, 8, 9]}
        ]
    }
