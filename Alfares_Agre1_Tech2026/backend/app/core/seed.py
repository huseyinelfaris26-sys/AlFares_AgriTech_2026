from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, date, timedelta
from passlib.context import CryptContext

from app.models import (
    User, Farm, Field, Crop, Sensor, PricingPlan, Drone, DroneMission, PestAlert
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database(session: AsyncSession):
    result = await session.execute(select(PricingPlan).limit(1))
    if result.scalar_one_or_none():
        print("✅ Database already seeded")
        return

    print("🌱 Seeding database...")

    plans = [
        PricingPlan(
            name="Starter", name_ar="البداية",
            description="Perfect for small farms",
            description_ar="مثالي للمزارع الصغيرة والمتوسطة",
            price_monthly=29.0, price_yearly=290.0,
            max_fields=5, max_drones=0, max_sensors=10,
            features={"crop_planning": True, "weather": True, "basic_irrigation": True, "mobile_app": True, "satellite_ndvi": False, "drone": False, "ai_pest": False, "iot_advanced": False, "support": "email"},
            features_ar={"تخطيط المحاصيل": True, "بيانات الطقس": True, "ري أساسي": True, "تطبيق الجوال": True, "NDVI أقمار صناعية": False, "طائرات مسيرة": False, "كشف آفات بالذكاء الاصطناعي": False, "IoT متقدم": False, "الدعم": "بريد إلكتروني"},
            is_popular=False, sort_order=1
        ),
        PricingPlan(
            name="Professional", name_ar="احترافي",
            description="For serious precision agriculture",
            description_ar="للزراعة الدقيقة المتقدمة",
            price_monthly=89.0, price_yearly=890.0,
            max_fields=25, max_drones=2, max_sensors=50,
            features={"crop_planning": True, "weather": True, "basic_irrigation": True, "precision_fertilization": True, "mobile_app": True, "satellite_ndvi": True, "drone": True, "ai_pest": True, "iot_advanced": True, "yield_prediction": True, "support": "priority"},
            features_ar={"تخطيط المحاصيل": True, "بيانات الطقس": True, "ري وتسميد دقيق": True, "تطبيق الجوال": True, "NDVI أقمار صناعية": True, "طائرات مسيرة": True, "كشف آفات بالذكاء الاصطناعي": True, "IoT متقدم": True, "تنبؤ الإنتاجية": True, "الدعم": "أولوية"},
            is_popular=True, sort_order=2
        ),
        PricingPlan(
            name="Enterprise", name_ar="المؤسسات",
            description="Full suite for large farms & agri-businesses",
            description_ar="حزمة كاملة للشركات والمزارع الكبيرة ووكلاء المعدات",
            price_monthly=249.0, price_yearly=2490.0,
            max_fields=999, max_drones=10, max_sensors=500,
            features={"crop_planning": True, "weather": True, "basic_irrigation": True, "precision_fertilization": True, "mobile_app": True, "satellite_ndvi": True, "drone": True, "ai_pest": True, "iot_advanced": True, "yield_prediction": True, "multi_farm": True, "api_access": True, "custom_reports": True, "dedicated_support": True, "white_label": True},
            features_ar={"تخطيط المحاصيل": True, "بيانات الطقس": True, "ري وتسميد دقيق": True, "تطبيق الجوال": True, "NDVI أقمار صناعية": True, "طائرات مسيرة": True, "كشف آفات بالذكاء الاصطناعي": True, "IoT متقدم": True, "تنبؤ الإنتاجية": True, "إدارة مزارع متعددة": True, "وصول API": True, "تقارير مخصصة": True, "دعم مخصص": True, "علامة بيضاء": True},
            is_popular=False, sort_order=3
        ),
    ]
    session.add_all(plans)

    farm = Farm(
        name="مزرعة الفارس النموذجية",
        owner_name="إدارة الفارس",
        location_name="تل أبيض، سوريا",
        latitude=36.52, longitude=37.15,
        total_area_hectares=35.8,
        description="مزرعة تجريبية لمنصة الفارس للزراعة الذكية"
    )
    session.add(farm)
    await session.flush()

    users = [
        User(email="admin@alfares.agri", hashed_password=pwd_context.hash("admin123"), full_name="مدير النظام", role="admin", farm_id=farm.id),
        User(email="farmer@alfares.agri", hashed_password=pwd_context.hash("farmer123"), full_name="مزارع تجريبي", role="farmer", farm_id=farm.id),
    ]
    session.add_all(users)

    fields_data = [
        {"name": "الحقل الشمالي", "area": 12.5, "crop": "قمح", "soil": "طيني لومي", "lat": 36.525, "lng": 37.148, "health": 91},
        {"name": "الحقل الجنوبي", "area": 8.3, "crop": "ذرة", "soil": "رملي طيني", "lat": 36.515, "lng": 37.155, "health": 78},
        {"name": "الحقل الشرقي", "area": 15.0, "crop": "قطن", "soil": "طيني", "lat": 36.522, "lng": 37.165, "health": 85},
    ]
    fields = []
    for fd in fields_data:
        f = Field(farm_id=farm.id, name=fd["name"], area_hectares=fd["area"], crop_type=fd["crop"],
                  soil_type=fd["soil"], latitude=fd["lat"], longitude=fd["lng"], health_score=fd["health"], status="active")
        session.add(f)
        fields.append(f)
    await session.flush()

    crops = [
        Crop(field_id=fields[0].id, name="قمح شتوي", scientific_name="Triticum aestivum", variety="شام 8",
             planting_date=date(2026, 11, 1), expected_harvest=date(2027, 5, 15), growth_stage="التفريع", target_yield=5.2, current_status="صحي"),
        Crop(field_id=fields[1].id, name="ذرة صفراء", scientific_name="Zea mays", variety="هجين محلي",
             planting_date=date(2026, 4, 10), expected_harvest=date(2026, 9, 20), growth_stage="النضج", target_yield=8.5, current_status="جيد"),
        Crop(field_id=fields[2].id, name="قطن", scientific_name="Gossypium hirsutum", variety="محلي محسن",
             planting_date=date(2026, 4, 20), expected_harvest=date(2026, 10, 10), growth_stage="تكوين اللوز", target_yield=3.5, current_status="صحي"),
    ]
    session.add_all(crops)

    for i, field in enumerate(fields):
        for j, depth in enumerate([15, 30, 45]):
            session.add(Sensor(field_id=field.id, sensor_code=f"SM-{field.id}-{j+1}", sensor_type="soil_moisture",
                               depth_cm=depth, is_online=True, battery_level=85 + i * 5, last_reading_at=datetime.utcnow()))

    drones = [
        Drone(farm_id=farm.id, name="فارس-1", model="DJI Mavic 3 Multispectral", serial_number="DJIM3M-2026-001",
              status="idle", battery_level=92, max_flight_time_min=43, camera_type="Multispectral", is_active=True),
        Drone(farm_id=farm.id, name="فارس-2", model="DJI Phantom 4 RTK", serial_number="DJIP4R-2026-002",
              status="charging", battery_level=45, max_flight_time_min=30, camera_type="RGB", is_active=True),
    ]
    session.add_all(drones)
    await session.flush()

    session.add(DroneMission(
        drone_id=drones[0].id, field_id=fields[0].id, mission_type="crop_health", status="completed",
        planned_start=datetime.utcnow() - timedelta(days=2),
        actual_start=datetime.utcnow() - timedelta(days=2, hours=1),
        actual_end=datetime.utcnow() - timedelta(days=2, minutes=25),
        altitude_m=80, overlap_percent=75, area_covered_ha=12.5, images_captured=148,
        notes="مسح صحة محصول القمح - NDVI جيد"
    ))

    session.add_all([
        PestAlert(field_id=fields[1].id, pest_name="من القمح (Aphids)", severity="medium", confidence=0.87,
                  status="active", recommended_action="رش مبيد حشري انتقائي + مراقبة يومية",
                  detected_at=datetime.utcnow() - timedelta(hours=5)),
        PestAlert(field_id=fields[2].id, pest_name="دودة اللوز الشوكية", severity="low", confidence=0.72,
                  status="monitoring", recommended_action="مراقبة أسبوعية",
                  detected_at=datetime.utcnow() - timedelta(days=1)),
    ])

    await session.commit()
    print("✅ Database seeded successfully!")
