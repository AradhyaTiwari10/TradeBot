"""Custom exceptions."""
from typing import Optional


class ValidationError(Exception):
    """Raised when input validation fails."""

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message or "Validation error")


class APIError(Exception):
    """Raised when an API call fails."""

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message or "API error")
