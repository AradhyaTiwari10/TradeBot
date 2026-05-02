"""Order execution engine.

Provides place_order which wraps Binance Futures order placement and
maps responses to typed dataclasses.
"""
from typing import Any

from .models import OrderRequest, OrderResponse
from .exceptions import ValidationError, APIError


def place_order(client: Any, order_request: OrderRequest) -> OrderResponse:
    """Place an order using the provided Binance client and return OrderResponse.

    Raises:
        ValidationError: for invalid input (e.g., LIMIT without price)
        APIError: for upstream API errors
    """
    try:
        if order_request.order_type.upper() == "MARKET":
            resp = client.futures_create_order(
                symbol=order_request.symbol,
                side=order_request.side,
                type="MARKET",
                quantity=order_request.quantity,
            )
        elif order_request.order_type.upper() == "LIMIT":
            if order_request.price is None:
                raise ValidationError("LIMIT orders require a price")
            resp = client.futures_create_order(
                symbol=order_request.symbol,
                side=order_request.side,
                type="LIMIT",
                quantity=order_request.quantity,
                price=order_request.price,
                timeInForce="GTC",
            )
        else:
            raise ValidationError(f"Unsupported order type: {order_request.order_type}")

        # Map response to OrderResponse
        order_id = int(resp.get("orderId"))
        status = resp.get("status")
        executed_qty = float(resp.get("executedQty", 0))
        avg_price_raw = resp.get("avgPrice")
        avg_price = float(avg_price_raw) if avg_price_raw not in (None, "") else None

        return OrderResponse(
            order_id=order_id,
            status=status,
            executed_qty=executed_qty,
            avg_price=avg_price,
        )

    except ValidationError:
        raise
    except Exception as exc:
        # Wrap any client/API error
        raise APIError(str(exc)) from exc
