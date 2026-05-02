"""Order execution."""
import logging
from typing import Any, Optional

from .models import OrderRequest, OrderResponse
from .validators import validate_order
from .exceptions import ValidationError, APIError


def place_order(client: Any, order_request: OrderRequest, exchange_rules: Optional[dict] = None) -> OrderResponse:
    """Submit order to exchange and return result.
    
    Raises:
        ValidationError: if order is invalid
        APIError: if exchange call fails
    """
    try:
        # perform validation (optionally using exchange rules provided by caller)
        validate_order(order_request, exchange_rules)

        order_type = order_request.order_type.upper()
        if order_type == "MARKET":
            logging.info(
                "Placing MARKET order %s %s %s",
                order_request.symbol,
                order_request.side,
                order_request.quantity,
            )
            resp = client.futures_create_order(
                symbol=order_request.symbol,
                side=order_request.side,
                type="MARKET",
                quantity=order_request.quantity,
            )
        elif order_type == "LIMIT":
            logging.info(
                "Placing LIMIT order %s %s %s @ %s",
                order_request.symbol,
                order_request.side,
                order_request.quantity,
                order_request.price,
            )
            resp = client.futures_create_order(
                symbol=order_request.symbol,
                side=order_request.side,
                type="LIMIT",
                quantity=order_request.quantity,
                price=order_request.price,
                timeInForce="GTC",
            )
        elif order_type == "STOP_LIMIT":
            logging.info(
                "Placing STOP_LIMIT order %s %s %s @ %s stop=%s",
                order_request.symbol,
                order_request.side,
                order_request.quantity,
                order_request.price,
                order_request.stop_price,
            )
            resp = client.futures_create_order(
                symbol=order_request.symbol,
                side=order_request.side,
                type="STOP",
                quantity=order_request.quantity,
                price=order_request.price,
                stopPrice=order_request.stop_price,
                timeInForce="GTC",
            )
        else:
            raise ValidationError(f"Unsupported order type: {order_type}")

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
        logging.error("Order error: %s", exc)
        raise APIError(str(exc)) from exc
