# ─── Stage 1: Builder ───────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─── Stage 2: Runtime ───────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app
# انسخ فقط المكتبات المصنّعة (بدون build tools)
COPY --from=builder /install /usr/local

# انسخ الكود
COPY main.py predictor.py model.py disease_info.json ./
COPY models/best_model.pth models/

# أمان: شغّل كمستخدم غير root
RUN useradd -m appuser
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
