"""Binance Futures Testnet client initialization."""
import os
from typing import Optional

from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

_EXCHANGE_INFO_CACHE = None


def get_client() -> Client:
    """Initialize and return Binance Futures Testnet client.

    Raises:
        ValueError: if API_KEY or API_SECRET environment variables are not set.
    """
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        raise ValueError(
            "Missing Binance API credentials. Set API_KEY and API_SECRET in the environment."
        )

    return Client(api_key, api_secret, testnet=True)


def get_exchange_info(client: Client) -> dict:
    """Fetch and cache futures exchange information from Binance.

    The result is cached in module scope to avoid repeated API calls.
    """
    global _EXCHANGE_INFO_CACHE
    if _EXCHANGE_INFO_CACHE is None:
        _EXCHANGE_INFO_CACHE = client.futures_exchange_info()
    return _EXCHANGE_INFO_CACHE


def get_symbol_rules(exchange_info: dict, symbol: str) -> Optional[dict]:
    """Extract simple symbol-specific trading rules from exchange_info.

    Returns a dict with keys: minQty, stepSize, tickSize, minPrice (all strings),
    or None if symbol not found.
    """
    target = symbol.upper()
    for s in exchange_info.get("symbols", []):
        if s.get("symbol") == target:
            filters = {f.get("filterType"): f for f in s.get("filters", [])}
            lot = filters.get("LOT_SIZE") or {}
            price = filters.get("PRICE_FILTER") or {}
            return {
                "minQty": lot.get("minQty"),
                "stepSize": lot.get("stepSize"),
                "minPrice": price.get("minPrice"),
                "tickSize": price.get("tickSize"),
            }
    return None


if __name__ == "__main__":
    client = get_client()
    print(client.futures_account_balance())
