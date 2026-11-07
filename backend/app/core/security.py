"""
Security & Evidence Ingestion Guard.
Provides strict file signature (magic byte) verification, extension matching,
size constraint enforcement, and filename sanitization.

Product: SCANNAI | Team: ROCKERZ

Security Architecture Notice:
Magic-byte and MIME header inspection establishes format consistency and prevents
file-extension masquerading (e.g., executing an executable renamed to .pdf).
It does NOT constitute full sandbox anti-malware scanning. Uploaded evidence
is treated as untrusted binary data, never executed, and isolated from executable paths.
"""

import os
import re
import hashlib
from typing import Tuple, Optional
from fastapi import UploadFile

from app.config import settings
from app.core.exceptions import (
    SecurityValidationError,
    FileTooLargeError,
    UnsupportedMediaTypeError,
)

# Known Magic-Byte Signatures for Allowed Evidence Types
MAGIC_SIGNATURES = {
    "pdf": [b"%PDF-"],
    "png": [b"\x89PNG\r\n\x1a\n"],
    "jpg": [b"\xff\xd8\xff"],
    "jpeg": [b"\xff\xd8\xff"],
}


def sanitize_filename(filename: Optional[str]) -> str:
    """
    Sanitizes user-provided filename to prevent path traversal and shell injection.
    Strips directory separators, null bytes, and non-whitelisted characters.
    """
    if not filename:
        return "unnamed_evidence"

    # Remove any directory path components
    basename = os.path.basename(filename)
    # Strip null bytes and control characters
    basename = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", basename)
    # Allow alphanumeric, hyphens, underscores, and single dot for extension
    clean = re.sub(r"[^\w\.\-]", "_", basename)
    # Limit length to prevent buffer or filesystem overflow
    return clean[:100] if clean else "unnamed_evidence"


def get_file_extension(filename: str) -> str:
    """Extracts lowercase file extension without the leading dot."""
    parts = filename.rsplit(".", 1)
    if len(parts) > 1:
        return parts[1].lower().strip()
    return ""


def verify_file_signature(header_bytes: bytes, extension: str) -> bool:
    """
    Validates whether the raw leading bytes match the claimed file extension.
    Special handling for RIFF/WEBP container format.
    """
    ext = extension.lower()
    if ext == "webp":
        # RIFF header: starts with 'RIFF' and contains 'WEBP' at offset 8
        return len(header_bytes) >= 12 and header_bytes[:4] == b"RIFF" and header_bytes[8:12] == b"WEBP"

    signatures = MAGIC_SIGNATURES.get(ext)
    if not signatures:
        return False

    return any(header_bytes.startswith(sig) for sig in signatures)


async def validate_evidence_file(file: UploadFile) -> Tuple[str, int, str, str]:
    """
    Performs comprehensive security ingestion checks:
    1. Validates declared filename and allowed extension.
    2. Validates declared MIME type against allowed list.
    3. Reads file stream in chunks to enforce size limits and compute SHA-256.
    4. Validates real file magic bytes against the declared extension.

    Returns:
        Tuple of (sanitized_filename, file_size_bytes, mime_type, sha256_hash)
    """
    raw_filename = file.filename or "unknown"
    clean_filename = sanitize_filename(raw_filename)
    ext = get_file_extension(clean_filename)

    # 1. Reject missing or disallowed extensions
    if not ext or ext not in settings.ALLOWED_EXTENSIONS:
        raise UnsupportedMediaTypeError(
            f"File extension '.{ext}' is not supported. Allowed formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # 2. Reject unsupported declared MIME types
    declared_mime = (file.content_type or "").lower()
    if declared_mime and declared_mime not in settings.ALLOWED_MIME_TYPES:
        raise UnsupportedMediaTypeError(
            f"MIME type '{declared_mime}' is not permitted. Allowed MIME types: {', '.join(settings.ALLOWED_MIME_TYPES)}"
        )

    # 3. Stream inspection: check size, verify magic bytes, compute SHA-256
    sha256 = hashlib.sha256()
    total_size = 0
    max_bytes = settings.max_upload_size_bytes
    header_bytes = b""

    # Chunk size: 64 KB
    chunk_size = 64 * 1024

    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break

        total_size += len(chunk)

        # Enforce maximum file size
        if total_size > max_bytes:
            raise FileTooLargeError(max_mb=settings.MAX_UPLOAD_SIZE_MB)

        # Retain initial 32 bytes for magic signature inspection
        if len(header_bytes) < 32:
            needed = 32 - len(header_bytes)
            header_bytes += chunk[:needed]

        sha256.update(chunk)

    # Empty file check
    if total_size == 0:
        raise SecurityValidationError("Submitted file is empty (0 bytes).")

    # 4. Verify magic bytes match declared extension
    if not verify_file_signature(header_bytes, ext):
        raise SecurityValidationError(
            f"File signature mismatch. The file content does not match the claimed extension '.{ext}'. "
            "Upload rejected to prevent file-masquerading attacks."
        )

    # Reset file cursor for downstream processing if needed
    await file.seek(0)

    computed_hash = sha256.hexdigest()
    effective_mime = declared_mime or f"application/{ext}"

    return clean_filename, total_size, effective_mime, computed_hash
