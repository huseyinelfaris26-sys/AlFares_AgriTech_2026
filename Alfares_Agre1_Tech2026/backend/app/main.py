from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.core.database import init_db, AsyncSessionLocal
from app.core.seed import seed_database
from app.api.routes import (
    fields, crops, irrigation, pests, weather, satellite, ai_analysis, auth, dashboard,
    pricing, drones
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    await init_db()
    async with AsyncSessionLocal() as session:
        await seed_database(session)
    yield
    print("👋 Shutting down Alfares Agri Tech...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="منصة الفارس للزراعة الذكية - Smart Agricultural Platform 2026",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix=f"{settings.API_PREFIX}/dashboard", tags=["Dashboard"])
app.include_router(fields.router, prefix=f"{settings.API_PREFIX}/fields", tags=["Fields Management"])
app.include_router(crops.router, prefix=f"{settings.API_PREFIX}/crops", tags=["Crop Planning"])
app.include_router(irrigation.router, prefix=f"{settings.API_PREFIX}/irrigation", tags=["Irrigation & Fertilization"])
app.include_router(pests.router, prefix=f"{settings.API_PREFIX}/pests", tags=["Pest & Disease Control"])
app.include_router(weather.router, prefix=f"{settings.API_PREFIX}/weather", tags=["Weather Data"])
app.include_router(satellite.router, prefix=f"{settings.API_PREFIX}/satellite", tags=["Satellite & Aerial"])
app.include_router(ai_analysis.router, prefix=f"{settings.API_PREFIX}/ai", tags=["AI Analysis"])
app.include_router(pricing.router, prefix=f"{settings.API_PREFIX}/pricing", tags=["Pricing Plans"])
app.include_router(drones.router, prefix=f"{settings.API_PREFIX}/drones", tags=["Drone Management"])

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "message": "مرحبًا بك في منصة الفارس للزراعة الذكية 2026",
        "docs": "/docs",
        "features": [
            "إدارة الحقول والمحاصيل",
            "الري والتسميد الدقيق",
            "كشف الآفات بالذكاء الاصطناعي",
            "بيانات الأقمار الصناعية",
            "تكامل الطائرات المسيرة",
            "خطط تسعير مرنة"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Alfares_Agreı_Tech2026"}
