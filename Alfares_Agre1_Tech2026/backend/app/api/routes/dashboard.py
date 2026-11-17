from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary():
    return {
        "farm_name": "مزرعة الفارس النموذجية",
        "total_fields": 12, "active_crops": 8, "health_score": 87.5, "alerts_count": 3,
        "irrigation_status": "optimal",
        "last_update": datetime.utcnow().isoformat(),
        "weather_summary": {"temp": 28.5, "humidity": 45, "condition": "مشمس", "rain_probability": 10},
        "productivity_trend": [
            {"month": "يناير", "value": 72}, {"month": "فبراير", "value": 78},
            {"month": "مارس", "value": 85}, {"month": "أبريل", "value": 81},
            {"month": "مايو", "value": 88}, {"month": "يونيو", "value": 92}
        ],
        "recent_alerts": [
            {"id": 1, "type": "pest", "message": "احتمال ظهور حشرات المن في الحقل 3", "severity": "medium", "time": "منذ ساعتين"},
            {"id": 2, "type": "irrigation", "message": "انخفاض رطوبة التربة في الحقل 7", "severity": "high", "time": "منذ 45 دقيقة"},
            {"id": 3, "type": "weather", "message": "توقع رياح قوية غدًا", "severity": "low", "time": "منذ 3 ساعات"}
        ]
    }

@router.get("/kpis")
async def get_kpis():
    return {
        "yield_prediction": 4.8, "water_efficiency": 92.3, "fertilizer_savings": 18.7,
        "pest_detection_accuracy": 94.1, "fields_under_monitoring": 12,
        "iot_sensors_online": 47, "satellite_images_this_week": 5
    }
