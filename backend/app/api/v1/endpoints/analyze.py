"""
Evidence Ingestion and Analysis Endpoint.
Receives suspicious communication text and/or evidence files,
validates integrity via security guard, and executes the deterministic rule engine.
Product: SCANNAI | Team: ROCKERZ
"""

import uuid
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, status
from app.core.security import validate_evidence_file
from app.core.exceptions import SecurityValidationError
from app.services.text_analyzer import analyze_text_communication
from app.models.schemas import (
    AnalysisResponse,
    EvidenceMetadata,
    EvidenceType,
    RiskClassification,
    ConfidenceLevel,
    RecommendedAction,
)

router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit Suspicious Communication or Evidence File",
    description="Validates submission integrity, verifies file magic bytes, and executes the forensic rule engine.",
)
async def analyze_evidence(
    message_text: Optional[str] = Form(None, description="Suspicious text or chat transcript"),
    case_reference: Optional[str] = Form(None, description="Optional user case reference"),
    ephemeral_mode: bool = Form(False, description="When true, evidence is processed in-memory only"),
    file: Optional[UploadFile] = File(None, description="Suspicious document (PDF) or screenshot (PNG/JPEG/WEBP)"),
) -> AnalysisResponse:
    """
    Validates submitted communication text and uploaded files.
    Enforces security boundaries and executes the deterministic procedural fallacy & threat analyzer.
    """
    if not message_text and not file:
        raise SecurityValidationError("At least one evidence item (message_text or file upload) must be provided.")

    evidence_items = []
    case_id = f"case_{uuid.uuid4().hex[:12]}"

    # Process text evidence
    has_text = bool(message_text and message_text.strip())
    if has_text:
        evidence_items.append(
            EvidenceMetadata(
                evidence_type=EvidenceType.TEXT,
                original_filename=None,
                file_size_bytes=len(message_text.encode("utf-8")),  # type: ignore[union-attr]
                mime_type="text/plain",
                sha256_hash=None,
            )
        )

    # Process file evidence with security guard
    if file:
        clean_name, size_bytes, mime, file_hash = await validate_evidence_file(file)
        ext = clean_name.rsplit(".", 1)[-1].lower() if "." in clean_name else ""
        ev_type = EvidenceType.DOCUMENT_PDF if ext == "pdf" else EvidenceType.SCREENSHOT_IMAGE

        evidence_items.append(
            EvidenceMetadata(
                evidence_type=ev_type,
                original_filename=clean_name,
                file_size_bytes=size_bytes,
                mime_type=mime,
                sha256_hash=file_hash,
            )
        )

    # Execute deterministic text & threat analysis if text is present
    if has_text:
        (
            risk_class,
            risk_score,
            confidence,
            summary,
            violations,
            indicators,
            limitations,
            actions,
        ) = analyze_text_communication(message_text)  # type: ignore[arg-type]

        return AnalysisResponse(
            case_id=case_id,
            risk_classification=risk_class,
            risk_score=risk_score,
            confidence_level=confidence,
            executive_summary=summary,
            procedural_violations=violations,
            detected_indicators=indicators,
            confidence_limitations=limitations,
            recommended_actions=actions,
            evidence_items=evidence_items,
        )

    # If only file is submitted (without text), perform format verification baseline
    return AnalysisResponse(
        case_id=case_id,
        risk_classification=RiskClassification.NEEDS_VERIFICATION,
        risk_score=50,
        confidence_level=ConfidenceLevel.MEDIUM,
        executive_summary="Evidence file successfully ingested and format-verified. Full visual & layout forensics will be applied in Phase 4.",
        procedural_violations=[],
        detected_indicators=[],
        confidence_limitations=[
            "File signature verified for format integrity. Visual OCR and document layout inspection are scheduled for Phase 4.",
        ],
        recommended_actions=[
            RecommendedAction(
                priority=1,
                category="IMMEDIATE_ACTION",
                action_text="Preserve original digital artifacts without altering timestamps.",
                helpline_or_portal="https://cybercrime.gov.in",
            )
        ],
        evidence_items=evidence_items,
    )
