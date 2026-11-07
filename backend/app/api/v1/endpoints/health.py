"""
Health and Diagnostic Endpoint.
Exposes public operational status without leaking environment variables,
internal paths, or credentials.
Product: SCANNAI | Team: ROCKERZ
"""

from fastapi import APIRouter
from app.config import settings
from app.models.schemas import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="System Health and Ingestion Capabilities",
    description="Returns operational health and supported evidence constraints without exposing internal secrets.",
)
async def check_health() -> HealthResponse:
    """
    Returns sanitized health status:
    - Service status and version
    - Runtime environment mode (development/production)
    - Supported upload limits and extensions
    No secrets, API keys, or raw system paths are returned.
    """
    return HealthResponse(
        status="healthy",
        application=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        ingestion_status={
            "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_MB,
            "allowed_extensions": settings.ALLOWED_EXTENSIONS,
            "supported_evidence_types": ["TEXT", "DOCUMENT_PDF", "SCREENSHOT_IMAGE"],
        },
    )
