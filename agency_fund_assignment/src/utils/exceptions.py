"""Custom exceptions for the application."""

from typing import Optional, Any, Dict


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        payload: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary."""
        return {
            "success": False,
            "error": self.message,
            **self.payload
        }


class DatabaseError(AppException):
    """Database operation failed."""

    def __init__(self, message: str = "Database operation failed", **kwargs):
        super().__init__(message, status_code=500, **kwargs)


class ExternalAPIError(AppException):
    """External API call failed."""

    def __init__(self, message: str = "External API call failed", **kwargs):
        super().__init__(message, status_code=502, **kwargs)


class NotFoundError(AppException):
    """Resource not found."""

    def __init__(self, resource: str = "Resource", **kwargs):
        message = f"{resource} not found"
        super().__init__(message, status_code=404, **kwargs)


class ValidationError(AppException):
    """Request validation failed."""

    def __init__(self, message: str = "Validation failed", **kwargs):
        super().__init__(message, status_code=400, **kwargs)


class GeminiNotConfiguredError(AppException):
    """Gemini API not configured."""

    def __init__(self, **kwargs):
        super().__init__(
            "Gemini API not configured. Please set GEMINI_API_KEY in environment.",
            status_code=503,
            **kwargs
        )
