"""
Structured Exceptions for SCANNAI.
Product: SCANNAI | Team: ROCKERZ
"""

from fastapi import HTTPException, status


class SecurityValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "SEC_VAL_FAILED", "message": detail},
        )


class FileTooLargeError(HTTPException):
    def __init__(self, max_mb: int):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "error_code": "FILE_TOO_LARGE",
                "message": f"Submitted file exceeds the maximum allowed upload limit of {max_mb} MB.",
            },
        )


class UnsupportedMediaTypeError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={"error_code": "UNSUPPORTED_MEDIA_TYPE", "message": detail},
        )
