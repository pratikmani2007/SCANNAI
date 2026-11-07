"""
Application Configuration Module.
Loads environment variables using Pydantic Settings with strict validation.
Product: SCANNAI | Team: ROCKERZ
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Application Info
    APP_NAME: str = "SCANNAI Core Forensic Engine"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Server Binding
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # CORS Policy
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    # Ingestion & File Security Limits
    MAX_UPLOAD_SIZE_MB: int = Field(default=25, ge=1, le=100)
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "png", "jpg", "jpeg", "webp"]
    ALLOWED_MIME_TYPES: List[str] = [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/webp",
    ]
    STORAGE_PATH: str = "backend/storage"

    # AI Configuration (Free Tier via Google AI Studio)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


settings = Settings()
