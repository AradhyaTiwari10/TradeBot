"""Custom exceptions used across the trading bot.

Keep exceptions simple and reusable; no business logic here.
"""

from typing import Optional


class ValidationError(Exception):
    """Raised when input validation fails."""

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message or "Validation error")


class APIError(Exception):
    """Raised when an upstream API or exchange returns an error."""

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message or "API error")
