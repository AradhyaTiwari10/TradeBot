"""Command-line interface for the trading bot built with Typer."""
from typing import Optional

import typer

from bot.client import get_client
from bot.models import OrderRequest
from bot.orders import place_order
from bot.exceptions import ValidationError, APIError

app = typer.Typer()


@app.command()
def trade(
    symbol: str = typer.Argument(...),
    side: str = typer.Argument(...),
    order_type: str = typer.Argument(...),
    quantity: float = typer.Argument(...),
    price: Optional[float] = typer.Argument(None),
) -> None:
    """Place an order on Binance Futures Testnet.

    Example: python cli.py trade BTCUSDT BUY MARKET 0.01
    """
    try:
        order = OrderRequest(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        client = get_client()
        result = place_order(client, order)

        # Exact output format required by spec
        print("Order Summary:")
        print()
        print(f"* Symbol: {order.symbol}")
        print(f"* Side: {order.side}")
        print(f"* Type: {order.order_type}")
        print(f"* Quantity: {order.quantity}")
        print()
        print("Result:")
        print()
        print(f"* Order ID: {result.order_id}")
        print(f"* Status: {result.status}")
        print(f"* Executed Qty: {result.executed_qty}")
        print(f"* Avg Price: {result.avg_price}")

    except (ValidationError, APIError) as exc:
        print(f"❌ Error: {exc}")
    except Exception as exc:  # pragma: no cover - unexpected errors
        print(f"❌ Error: {exc}")


if __name__ == "__main__":
    app()
