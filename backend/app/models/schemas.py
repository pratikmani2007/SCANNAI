"""
Domain Schemas and Data Contracts for SCANNAI.
Product: SCANNAI | Team: ROCKERZ
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator


class EvidenceType(str, Enum):
    TEXT = "TEXT"
    DOCUMENT_PDF = "DOCUMENT_PDF"
    SCREENSHOT_IMAGE = "SCREENSHOT_IMAGE"
    AUDIO_RECORDING = "AUDIO_RECORDING"
    VIDEO_RECORDING = "VIDEO_RECORDING"


class RiskClassification(str, Enum):
    LOW_RISK = "LOW RISK"
    NEEDS_VERIFICATION = "NEEDS VERIFICATION"
    HIGH_RISK = "HIGH RISK"


class ConfidenceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY HIGH"


class IndicatorSeverity(str, Enum):
    INFORMATIONAL = "INFORMATIONAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SuspiciousIndicator(BaseModel):
    category: str = Field(..., description="E.g., Coercion, Impersonation, Document Inconsistency, Payment Anomalies")
    severity: IndicatorSeverity = Field(..., description="Severity classification of the indicator")
    title: str = Field(..., description="Concise headline describing the anomaly")
    description: str = Field(..., description="Detailed technical or linguistic breakdown of the finding")
    evidence_citation: Optional[str] = Field(None, description="Specific quotation or visual region from submitted evidence")


class ProceduralViolation(BaseModel):
    code: str = Field(..., description="Unique procedural fallacy code (e.g., PROC-IND-01)")
    official_norm: str = Field(..., description="The verified real-world policy of law enforcement or banks")
    observed_violation: str = Field(..., description="How the communication contradicts legitimate procedure")
    jurisdiction: str = Field(default="IN", description="Jurisdictional context (e.g., IN, US, UK, GLOBAL)")


class RecommendedAction(BaseModel):
    priority: int = Field(..., ge=1, le=10, description="Execution priority (1 being immediate)")
    category: str = Field(..., description="IMMEDIATE_ACTION, VERIFICATION, REPORTING, or ADVISORY")
    action_text: str = Field(..., description="Clear, non-technical prescriptive guidance for the user")
    helpline_or_portal: Optional[str] = Field(None, description="Official portal link or verified emergency helpline (e.g., 1930)")


class EvidenceMetadata(BaseModel):
    evidence_type: EvidenceType
    original_filename: Optional[str] = None
    file_size_bytes: Optional[int] = Field(None, ge=0)
    mime_type: Optional[str] = None
    sha256_hash: Optional[str] = Field(None, min_length=64, max_length=64)
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnalysisRequest(BaseModel):
    message_text: Optional[str] = Field(
        None,
        max_length=50000,
        description="Raw suspicious communication text, transcript, or WhatsApp chat export"
    )
    case_reference: Optional[str] = Field(
        None,
        max_length=100,
        description="Optional investigator case reference or user tracking tag"
    )
    ephemeral_mode: bool = Field(
        default=False,
        description="When true, evidence is analyzed in-memory and immediately discarded without persistence"
    )

    @field_validator("message_text")
    @classmethod
    def validate_content_presence(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            return None
        return v


class AnalysisResponse(BaseModel):
    case_id: str = Field(..., description="Unique investigation identifier (UUIDv4 or prefixed hex)")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    risk_classification: RiskClassification = Field(..., description="Primary 3-tier risk outcome")
    risk_score: Optional[int] = Field(None, ge=0, le=100, description="Normalized risk index (0-100)")
    confidence_level: ConfidenceLevel = Field(..., description="Model and heuristic confidence")
    executive_summary: str = Field(..., description="Calm, objective narrative explaining the findings")
    procedural_violations: List[ProceduralViolation] = Field(default_factory=list)
    detected_indicators: List[SuspiciousIndicator] = Field(default_factory=list)
    confidence_limitations: List[str] = Field(
        default_factory=list,
        description="Explicit caveats clarifying what cannot be determined with 100% certainty"
    )
    recommended_actions: List[RecommendedAction] = Field(default_factory=list)
    evidence_items: List[EvidenceMetadata] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Operational status")
    application: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    environment: str = Field(..., description="Runtime environment (development/production)")
    ingestion_status: Dict[str, Any] = Field(..., description="Capabilities and format constraints")
