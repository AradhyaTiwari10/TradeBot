"""Validation helpers for trading inputs.

Keep validation separate from business logic. Validators raise
ValidationError on failure.
"""
from typing import Iterable

from .models import OrderRequest
from .exceptions import ValidationError


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def _ensure_in(value: str, allowed: Iterable[str], name: str) -> None:
    if value.upper() not in allowed:
        raise ValidationError(f"Invalid {name}: {value}. Allowed: {', '.join(sorted(allowed))}")


def _ensure_positive(number: float, name: str) -> None:
    try:
        if float(number) <= 0:
            raise ValidationError(f"{name} must be positive")
    except (TypeError, ValueError):
        raise ValidationError(f"{name} must be a number")


def validate_order_request(order: OrderRequest) -> None:
    """Validate an OrderRequest in-place. Raises ValidationError on failure."""
    if not isinstance(order, OrderRequest):
        raise ValidationError("Invalid order object")

    _ensure_in(order.side, VALID_SIDES, "side")
    _ensure_in(order.order_type, VALID_ORDER_TYPES, "order_type")
    _ensure_positive(order.quantity, "quantity")

    if order.order_type.upper() == "LIMIT":
        if order.price is None:
            raise ValidationError("LIMIT orders require a price")
        _ensure_positive(order.price, "price")
