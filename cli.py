"""CLI interface for order placement."""
from typing import Optional

import typer

from bot.client import get_client, get_exchange_info, get_symbol_rules
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

    Example: python cli.py trade BTCUSDT BUY MARKET 0.01
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

        client = get_client()
        exchange_info = get_exchange_info(client)
        rules = get_symbol_rules(exchange_info, order.symbol)

        validate_order(order, rules)
        result = place_order(client, order, rules)

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


@app.command()
def info(symbol: str = typer.Argument(...)) -> None:
    """Show symbol trading rules (minQty, stepSize, tickSize, minPrice)."""
    try:
        client = get_client()
        exchange_info = get_exchange_info(client)
        rules = get_symbol_rules(exchange_info, symbol)

        if not rules:
            print(f"No trading rules found for symbol: {symbol}")
            return

        print("---")
        print(f"Symbol: {symbol.upper()}\n")
        print(f"minQty   : {rules.get('minQty')}")
        print(f"stepSize : {rules.get('stepSize')}")
        print(f"tickSize : {rules.get('tickSize')}")
        print(f"minPrice : {rules.get('minPrice')}\n")

    except Exception as exc:
        print("---")
        print("Error\n")
        print(f"Message: {exc}\n")


if __name__ == "__main__":
    setup_logging()
    app()
