"""
Tests for Core Pydantic Schemas.
Product: SCANNAI | Team: ROCKERZ
"""

import pytest
from pydantic import ValidationError
from app.models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    RiskClassification,
    ConfidenceLevel,
    IndicatorSeverity,
    SuspiciousIndicator,
    ProceduralViolation,
    RecommendedAction,
    EvidenceType,
    EvidenceMetadata,
)


def test_analysis_request_valid():
    req = AnalysisRequest(message_text="You are under digital arrest. Pay 50000 immediately.")
    assert req.message_text == "You are under digital arrest. Pay 50000 immediately."
    assert req.ephemeral_mode is False


def test_analysis_request_whitespace_stripping():
    req = AnalysisRequest(message_text="   ")
    assert req.message_text is None


def test_analysis_response_structure():
    resp = AnalysisResponse(
        case_id="case_12345",
        risk_classification=RiskClassification.HIGH_RISK,
        risk_score=95,
        confidence_level=ConfidenceLevel.VERY_HIGH,
        executive_summary="Digital arrest scam detected.",
        procedural_violations=[
            ProceduralViolation(
                code="PROC-IND-01",
                official_norm="Police do not arrest via video call",
                observed_violation="Threatened arrest over WhatsApp",
                jurisdiction="IN",
            )
        ],
        detected_indicators=[
            SuspiciousIndicator(
                category="Coercion",
                severity=IndicatorSeverity.CRITICAL,
                title="Immediate Arrest Threat",
                description="Scammer demanded victim remain on video call.",
            )
        ],
        confidence_limitations=["Textual analysis based on submitted transcript."],
        recommended_actions=[
            RecommendedAction(
                priority=1,
                category="IMMEDIATE_ACTION",
                action_text="Terminate call immediately.",
                helpline_or_portal="1930",
            )
        ],
        evidence_items=[
            EvidenceMetadata(
                evidence_type=EvidenceType.TEXT,
                file_size_bytes=100,
                mime_type="text/plain",
            )
        ],
    )
    assert resp.risk_classification == RiskClassification.HIGH_RISK
    assert resp.risk_score == 95
    assert len(resp.procedural_violations) == 1
    assert len(resp.detected_indicators) == 1


def test_risk_score_bounds_validation():
    with pytest.raises(ValidationError):
        AnalysisResponse(
            case_id="case_invalid",
            risk_classification=RiskClassification.LOW_RISK,
            risk_score=150,  # Invalid: > 100
            confidence_level=ConfidenceLevel.LOW,
            executive_summary="Invalid score test",
        )
