"""
V1 API Router Aggregator.
Product: SCANNAI | Team: ROCKERZ
"""

from fastapi import APIRouter
from app.api.v1.endpoints import health, analyze

api_router = APIRouter()

api_router.include_router(health.router, tags=["System Health"])
api_router.include_router(analyze.router, tags=["Forensic Ingestion & Analysis"])
