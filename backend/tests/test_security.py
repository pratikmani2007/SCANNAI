"""
Tests for Security Ingestion Guard & Magic Byte Verification.
Product: SCANNAI | Team: ROCKERZ
"""

import io
import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient
from main import app
from app.core.security import (
    sanitize_filename,
    verify_file_signature,
    validate_evidence_file,
)
from app.core.exceptions import (
    SecurityValidationError,
    UnsupportedMediaTypeError,
)

client = TestClient(app)


def test_filename_sanitization_removes_traversal():
    assert sanitize_filename("../../../malicious.pdf") == "malicious.pdf"
    assert sanitize_filename("..\\..\\warrant.pdf") == "warrant.pdf"
    assert sanitize_filename("safe_document_123.pdf") == "safe_document_123.pdf"
    assert sanitize_filename(None) == "unnamed_evidence"


def test_verify_file_signature_pdf():
    valid_pdf_header = b"%PDF-1.7\r\n..."
    assert verify_file_signature(valid_pdf_header, "pdf") is True

    fake_pdf_header = b"This is just plain text masquerading as a pdf"
    assert verify_file_signature(fake_pdf_header, "pdf") is False


def test_verify_file_signature_png():
    valid_png_header = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    assert verify_file_signature(valid_png_header, "png") is True

    fake_png_header = b"NOT_A_PNG_HEADER"
    assert verify_file_signature(fake_png_header, "png") is False


def test_verify_file_signature_jpeg():
    valid_jpeg_header = b"\xff\xd8\xff\xe0\x00\x10JFIF"
    assert verify_file_signature(valid_jpeg_header, "jpg") is True
    assert verify_file_signature(valid_jpeg_header, "jpeg") is True


@pytest.mark.asyncio
async def test_validate_evidence_file_rejects_unsupported_ext():
    file = UploadFile(filename="script.exe", file=io.BytesIO(b"MZ\x90\x00"))
    with pytest.raises(UnsupportedMediaTypeError):
        await validate_evidence_file(file)


@pytest.mark.asyncio
async def test_validate_evidence_file_rejects_empty_file():
    file = UploadFile(filename="empty.pdf", file=io.BytesIO(b""))
    with pytest.raises(SecurityValidationError):
        await validate_evidence_file(file)


@pytest.mark.asyncio
async def test_validate_evidence_file_rejects_masquerading_file():
    # File named .pdf but containing arbitrary text
    file = UploadFile(
        filename="fake_summons.pdf",
        file=io.BytesIO(b"Plain text claiming to be a PDF warrant"),
    )
    with pytest.raises(SecurityValidationError) as exc_info:
        await validate_evidence_file(file)
    assert "signature mismatch" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
async def test_validate_evidence_file_accepts_valid_pdf():
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
    file = UploadFile(filename="legit_warrant.pdf", file=io.BytesIO(pdf_content))
    clean_name, size, mime, sha256_hash = await validate_evidence_file(file)

    assert clean_name == "legit_warrant.pdf"
    assert size == len(pdf_content)
    assert len(sha256_hash) == 64


def test_api_analyze_with_text():
    response = client.post(
        "/api/v1/analyze",
        data={"message_text": "CBI Officer calling. Transfer verification deposit."},
    )
    assert response.status_code == 200
    data = response.json()
    assert "case_id" in data
    assert data["risk_classification"] == "HIGH RISK"
    assert len(data["procedural_violations"]) >= 1
    assert len(data["evidence_items"]) == 1
    assert data["evidence_items"][0]["evidence_type"] == "TEXT"


def test_api_analyze_with_valid_pdf_file():
    pdf_content = b"%PDF-1.5\n%Header\n%%EOF"
    response = client.post(
        "/api/v1/analyze",
        data={"case_reference": "REF-001"},
        files={"file": ("warrant.pdf", pdf_content, "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["evidence_items"]) == 1
    assert data["evidence_items"][0]["evidence_type"] == "DOCUMENT_PDF"
    assert data["evidence_items"][0]["original_filename"] == "warrant.pdf"


def test_api_analyze_rejects_masqueraded_file():
    fake_content = b"This is not a real PDF file"
    response = client.post(
        "/api/v1/analyze",
        files={"file": ("warrant.pdf", fake_content, "application/pdf")},
    )
    assert response.status_code == 400
    assert "signature mismatch" in response.text.lower()
