from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "admin@alfares.agri": {
        "id": 1, "email": "admin@alfares.agri", "full_name": "مدير النظام",
        "hashed_password": pwd_context.hash("admin123"), "role": "admin", "farm_id": None
    },
    "farmer@alfares.agri": {
        "id": 2, "email": "farmer@alfares.agri", "full_name": "مزارع تجريبي",
        "hashed_password": pwd_context.hash("farmer123"), "role": "farmer", "farm_id": 1
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "farmer"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest):
    user = fake_users_db.get(credentials.email)
    if not user or not pwd_context.verify(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="بيانات الدخول غير صحيحة")
    token = create_access_token({"sub": user["email"], "role": user["role"], "id": user["id"]})
    return {
        "access_token": token, "token_type": "bearer",
        "user": {"id": user["id"], "email": user["email"], "full_name": user["full_name"], "role": user["role"], "farm_id": user["farm_id"]}
    }

@router.post("/register")
async def register(user_data: UserCreate):
    if user_data.email in fake_users_db:
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مستخدم مسبقًا")
    new_user = {
        "id": len(fake_users_db) + 1, "email": user_data.email, "full_name": user_data.full_name,
        "hashed_password": pwd_context.hash(user_data.password), "role": user_data.role, "farm_id": None
    }
    fake_users_db[user_data.email] = new_user
    return {"message": "تم التسجيل بنجاح", "user_id": new_user["id"]}
