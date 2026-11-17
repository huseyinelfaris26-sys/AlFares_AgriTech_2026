from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    APP_NAME: str = "Alfares Agri Tech 2026"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    
    # Database - SQLite for easy demo
    DATABASE_URL: str = "sqlite+aiosqlite:///./alfares_agri.db"
    
    SECRET_KEY: str = "alfares-agri-tech-2026-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000"
    ]
    
    WEATHER_API_KEY: Optional[str] = None
    SATELLITE_API_KEY: Optional[str] = None
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    REDIS_URL: str = "redis://localhost:6379/0"
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
