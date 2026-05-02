"""CLI interface for order placement."""
from typing import Optional

import typer

from bot.client import get_client
from bot.models import OrderRequest
from bot.orders import place_order
from bot.validators import validate_order
from bot.exceptions import ValidationError, APIError
from bot.logging_config import setup_logging

app = typer.Typer()


@app.command()
def trade(
    symbol: str = typer.Argument(...),
    side: str = typer.Argument(...),
    order_type: str = typer.Argument(...),
    quantity: float = typer.Argument(...),
    price: Optional[float] = typer.Argument(None),
    stop_price: Optional[float] = typer.Argument(None),
) -> None:
    """Place an order on Binance Futures Testnet.
    
    Example: python cli.py BTCUSDT BUY MARKET 0.01
    """
    try:
        order = OrderRequest(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
        )

        validate_order(order)
        client = get_client()
        result = place_order(client, order)

        print("---")
        print("## Order Summary\n")
        print(f"Symbol      : {order.symbol}")
        print(f"Side        : {order.side}")
        print(f"Type        : {order.order_type}")
        print(f"Quantity    : {order.quantity}\n")
        print("---\n")
        print("## Result\n")
        print(f"Order ID    : {result.order_id}")
        print(f"Status      : {result.status}")
        print(f"Executed Qty: {result.executed_qty}")
        print(f"Avg Price   : {result.avg_price}\n")

    except (ValidationError, APIError) as exc:
        print("---")
        print("Error\n")
        print(f"Message: {exc}\n")
    except Exception as exc:
        print("---")
        print("Error\n")
        print(f"Message: {exc}\n")


if __name__ == "__main__":
    setup_logging()
    app()
