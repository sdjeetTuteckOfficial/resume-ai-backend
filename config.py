# ==================== config.py ====================
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # SMTP
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    FROM_EMAIL: str

    # OTP
    OTP_EXPIRE_MINUTES: int = 10
    
    class Config:
        env_file = ".env"   # loads values automatically from .env

settings = Settings()
