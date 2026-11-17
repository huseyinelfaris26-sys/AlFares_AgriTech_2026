from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/current")
async def current_weather(lat: float = 36.52, lng: float = 37.15):
    return {
        "location": {"lat": lat, "lng": lng, "name": "تل أبيض / محيط المزرعة"},
        "timestamp": datetime.utcnow().isoformat(),
        "temperature_c": round(random.uniform(18, 32), 1),
        "feels_like": round(random.uniform(17, 33), 1),
        "humidity": random.randint(30, 70),
        "wind_speed_kmh": round(random.uniform(5, 25), 1),
        "wind_direction": random.choice(["شمال", "شمال شرقي", "شرقي", "جنوب شرقي"]),
        "condition": random.choice(["مشمس", "غائم جزئيًا", "صافي", "غائم"]),
        "pressure_hpa": random.randint(1010, 1025),
        "uv_index": random.randint(3, 9),
        "visibility_km": round(random.uniform(8, 15), 1)
    }

@router.get("/forecast")
async def weather_forecast(days: int = 7, lat: float = 36.52, lng: float = 37.15):
    forecast = []
    base = datetime.utcnow()
    for i in range(days):
        day = base + timedelta(days=i)
        forecast.append({
            "date": day.strftime("%Y-%m-%d"), "day_name": day.strftime("%A"),
            "temp_max": round(random.uniform(22, 34), 1), "temp_min": round(random.uniform(10, 20), 1),
            "humidity": random.randint(35, 65), "rain_probability": random.randint(0, 40),
            "rain_mm": round(random.uniform(0, 5), 1) if random.random() > 0.7 else 0,
            "condition": random.choice(["مشمس", "غائم جزئيًا", "ممطر خفيف", "صافي"]),
            "wind_kmh": round(random.uniform(8, 30), 1)
        })
    return {"location": {"lat": lat, "lng": lng}, "generated_at": datetime.utcnow().isoformat(), "forecast": forecast}

@router.get("/alerts")
async def weather_alerts():
    return {
        "alerts": [{
            "type": "wind", "severity": "medium",
            "message": "توقعات برياح قوية تصل إلى 40 كم/س يوم غد",
            "valid_from": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
            "valid_to": (datetime.utcnow() + timedelta(hours=36)).isoformat()
        }]
    }
