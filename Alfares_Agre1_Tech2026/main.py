from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from fastapi.concurrency import run_in_threadpool
import torch

# ─── Lifespan (التحميل مرة واحدة) ──────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # تحميل النموذج مرة واحدة عند الإقلاع
    global predictor
    predictor = DiseasePredictor(model_path="models/best_model.pth")
    # Warm-up: استدعاء وهمي لتسخين الذاكرة
    _dummy = torch.zeros(1, 3, 224, 224).to(predictor.device)
    with torch.inference_mode():  # ⚡ أسرع من no_grad
        predictor.model(_dummy)
    yield
    # Cleanup عند الإيقاف
    del predictor

app = FastAPI(title="AgriAI API", lifespan=lifespan)

# ─── Security ───────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],  # ⚠️ لا تستخدم *
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ─── Health Checks (لـ Load Balancer) ───────────────────
@app.get("/healthz")
def liveness():
    """هل الخادم حي؟"""
    return {"status": "alive"}

@app.get("/readyz")
def readiness():
    """هل النموذج جاهز للاستقبال؟"""
    return {"ready": predictor is not None, "device": str(predictor.device)}

# ─── Prediction (Thread Pool لتجنب حجب Event Loop) ──────
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    if len(contents) > 8 * 1024 * 1024:
        raise HTTPException(413, "File too large (max 8MB)")

    # ⚡ run_in_threadpool: لا يحجب الـ event loop
    result = await run_in_threadpool(predictor.predict, contents)
    return result
