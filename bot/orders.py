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
        # Validate order before calling the exchange
        from .validators import validate_order_request
        import logging

        validate_order_request(order_request)

        # Log the outgoing request (do not include secrets)
        logging.info(
            "Placing %s order %s %s %s %s",
            order_request.order_type.upper(),
            order_request.symbol,
            order_request.side,
            order_request.quantity,
            order_request.price,
        )

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

        logging.info("Order Success ID=%s Status=%s", order_id, status)

        return OrderResponse(
            order_id=order_id,
            status=status,
            executed_qty=executed_qty,
            avg_price=avg_price,
        )

    except ValidationError:
        raise
    except Exception as exc:
        # Log the error and wrap it
        import logging

        logging.error("Order error: %s", exc)
        raise APIError(str(exc)) from exc
