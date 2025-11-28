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
    
    # API KEY
    # Define as lowercase. Pydantic reads 'GOOGLE_API_KEY' from env and maps it here.
    google_api_key: str 
    
    class Config:
        env_file = ".env"   # loads values automatically from .env
        extra = "ignore"    # Prevents errors if .env has variables not defined here

settings = Settings()