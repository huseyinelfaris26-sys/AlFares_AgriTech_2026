from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/ndvi/{field_id}")
async def get_ndvi(field_id: str):
    history = []
    base = datetime.utcnow()
    for i in range(8):
        day = base - timedelta(days=i*7)
        history.append({
            "date": day.strftime("%Y-%m-%d"),
            "ndvi_mean": round(random.uniform(0.45, 0.85), 3),
            "ndvi_min": round(random.uniform(0.2, 0.5), 3),
            "ndvi_max": round(random.uniform(0.7, 0.95), 3),
            "cloud_cover": round(random.uniform(0, 25), 1)
        })
    return {
        "field_id": field_id, "latest_ndvi": history[0]["ndvi_mean"],
        "trend": "improving" if history[0]["ndvi_mean"] > history[1]["ndvi_mean"] else "stable",
        "history": list(reversed(history)),
        "interpretation": "قيم NDVI جيدة تشير إلى صحة نباتية مرتفعة"
    }

@router.get("/images/{field_id}")
async def list_satellite_images(field_id: str):
    return {
        "field_id": field_id,
        "images": [
            {"id": "sat-001", "date": "2026-11-15", "source": "Sentinel-2", "resolution_m": 10,
             "bands": ["B02", "B03", "B04", "B08"], "cloud_cover": 5.2, "url": "/uploads/satellite/sample_ndvi.png", "type": "NDVI"},
            {"id": "sat-002", "date": "2026-11-10", "source": "Sentinel-2", "resolution_m": 10,
             "cloud_cover": 12.8, "url": "/uploads/satellite/sample_rgb.png", "type": "True Color"}
        ]
    }

@router.get("/hail-detection")
async def hail_detection(lat: float = 36.52, lng: float = 37.15):
    risk = random.choice(["low", "low", "medium", "high"])
    return {
        "location": {"lat": lat, "lng": lng}, "hail_risk": risk,
        "probability": {"low": 15, "medium": 45, "high": 75}.get(risk, 20),
        "valid_until": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
        "recommendation": "تأمين المحاصيل الحساسة" if risk == "high" else "مراقبة الطقس"
    }
