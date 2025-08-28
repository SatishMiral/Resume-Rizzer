# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    # FastAPI
    PROJECT_NAME: str = "Resume Rizzer"

    class Config:
        env_file = ".env"
        extra = "ignore"  # ignore extra keys if accidentally added in .env

settings = Settings()
