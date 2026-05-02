from typing import Iterable, Optional
from decimal import Decimal, getcontext

from .models import OrderRequest
from .exceptions import ValidationError

getcontext().prec = 18

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_LIMIT"}


def _ensure_in(value: str, allowed: Iterable[str], name: str) -> None:
    if value.upper() not in allowed:
        raise ValidationError(f"Invalid {name}: {value}. Allowed: {', '.join(sorted(allowed))}")


def _ensure_positive(number: float, name: str) -> None:
    try:
        if Decimal(str(number)) <= 0:
            raise ValidationError(f"{name} must be positive")
    except (TypeError, ValueError, ArithmeticError):
        raise ValidationError(f"{name} must be a number")


def _is_multiple(value: Decimal, step: Decimal) -> bool:
    try:
        return (value % step) == 0
    except (ArithmeticError, ValueError):
        return False


def _validate_against_rules(order: OrderRequest, rules: dict) -> None:
    """Validate quantity and price against exchange symbol rules."""
    if not rules:
        return

    try:
        min_qty = Decimal(rules.get("minQty")) if rules.get("minQty") else None
        step = Decimal(rules.get("stepSize")) if rules.get("stepSize") else None
        min_price = Decimal(rules.get("minPrice")) if rules.get("minPrice") else None
        tick = Decimal(rules.get("tickSize")) if rules.get("tickSize") else None
    except (TypeError, ArithmeticError, ValueError):
        # If parsing fails, skip exchange-aware validation
        return

    q = Decimal(str(order.quantity))
    if min_qty is not None and q < min_qty:
        raise ValidationError("Quantity below minimum allowed")
    if step and not _is_multiple(q, step):
        raise ValidationError("Invalid step size for quantity")

    if order.order_type.upper() in ("LIMIT", "STOP_LIMIT"):
        if order.price is None:
            raise ValidationError("Price required for this order type")
        p = Decimal(str(order.price))
        if min_price is not None and p < min_price:
            raise ValidationError("Price below minimum allowed")
        if tick and not _is_multiple(p, tick):
            raise ValidationError("Price does not match tick size")


def validate_order(order: OrderRequest, exchange_rules: Optional[dict] = None) -> None:
    """Validate order fields before submission.

    If exchange_rules is provided, perform symbol-specific checks.
    """
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

    # Exchange-aware validation
    if exchange_rules:
        _validate_against_rules(order, exchange_rules)
