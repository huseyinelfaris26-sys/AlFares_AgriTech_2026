from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.pricing import PricingPlan, Subscription

router = APIRouter()

class SubscribeRequest(BaseModel):
    plan_id: int
    billing_cycle: str = "monthly"
    user_id: int = 2

@router.get("/plans")
async def list_plans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PricingPlan).where(PricingPlan.is_active == True).order_by(PricingPlan.sort_order))
    plans = result.scalars().all()
    return [
        {
            "id": p.id, "name": p.name, "name_ar": p.name_ar, "description": p.description,
            "description_ar": p.description_ar, "price_monthly": p.price_monthly, "price_yearly": p.price_yearly,
            "currency": p.currency, "max_fields": p.max_fields, "max_drones": p.max_drones, "max_sensors": p.max_sensors,
            "features": p.features, "features_ar": p.features_ar, "is_popular": p.is_popular,
            "savings_yearly_percent": round((1 - (p.price_yearly / (p.price_monthly * 12))) * 100)
        }
        for p in plans
    ]

@router.get("/plans/{plan_id}")
async def get_plan(plan_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PricingPlan).where(PricingPlan.id == plan_id))
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="الخطة غير موجودة")
    return {
        "id": plan.id, "name_ar": plan.name_ar, "price_monthly": plan.price_monthly,
        "price_yearly": plan.price_yearly, "features_ar": plan.features_ar,
        "max_fields": plan.max_fields, "max_drones": plan.max_drones, "max_sensors": plan.max_sensors
    }

@router.post("/subscribe")
async def subscribe(req: SubscribeRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PricingPlan).where(PricingPlan.id == req.plan_id))
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="الخطة غير موجودة")
    end_date = datetime.utcnow() + (timedelta(days=365) if req.billing_cycle == "yearly" else timedelta(days=30))
    sub = Subscription(user_id=req.user_id, plan_id=req.plan_id, status="active",
                       billing_cycle=req.billing_cycle, start_date=datetime.utcnow(), end_date=end_date, auto_renew=True)
    db.add(sub)
    await db.flush()
    return {
        "message": f"تم الاشتراك بنجاح في خطة {plan.name_ar}", "subscription_id": sub.id,
        "plan": plan.name_ar, "billing_cycle": req.billing_cycle, "end_date": end_date.isoformat(),
        "amount": plan.price_yearly if req.billing_cycle == "yearly" else plan.price_monthly
    }

@router.get("/my-subscription/{user_id}")
async def my_subscription(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user_id, Subscription.status == "active")
        .order_by(Subscription.created_at.desc())
    )
    sub = result.scalar_one_or_none()
    if not sub:
        return {"has_subscription": False, "message": "لا يوجد اشتراك نشط"}
    plan_result = await db.execute(select(PricingPlan).where(PricingPlan.id == sub.plan_id))
    plan = plan_result.scalar_one()
    return {
        "has_subscription": True, "plan_name": plan.name_ar, "status": sub.status,
        "billing_cycle": sub.billing_cycle, "start_date": sub.start_date.isoformat(),
        "end_date": sub.end_date.isoformat() if sub.end_date else None, "auto_renew": sub.auto_renew
  }
