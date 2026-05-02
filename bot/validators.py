"""Input validation for orders."""
from typing import Iterable

from .models import OrderRequest
from .exceptions import ValidationError


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_LIMIT"}


def _ensure_in(value: str, allowed: Iterable[str], name: str) -> None:
    """Check that value (case-insensitive) is in allowed set."""
    if value.upper() not in allowed:
        raise ValidationError(f"Invalid {name}: {value}. Allowed: {', '.join(sorted(allowed))}")


def _ensure_positive(number: float, name: str) -> None:
    """Verify that number is positive."""
    try:
        if float(number) <= 0:
            raise ValidationError(f"{name} must be positive")
    except (TypeError, ValueError):
        raise ValidationError(f"{name} must be a number")


def validate_order(order: OrderRequest) -> None:
    """Validate order fields before submission."""
    if not isinstance(order, OrderRequest):
        raise ValidationError("Invalid order object")

    _ensure_in(order.side, VALID_SIDES, "side")
    _ensure_in(order.order_type, VALID_ORDER_TYPES, "order_type")
    _ensure_positive(order.quantity, "quantity")

    if order.order_type.upper() == "LIMIT":
        if order.price is None:
            raise ValidationError("LIMIT orders require a price")
        _ensure_positive(order.price, "price")
    if order.order_type.upper() == "STOP_LIMIT":
        if order.price is None:
            raise ValidationError("STOP_LIMIT orders require a price")
        if order.stop_price is None:
            raise ValidationError("STOP_LIMIT orders require a stop_price")
        _ensure_positive(order.price, "price")
        _ensure_positive(order.stop_price, "stop_price")
