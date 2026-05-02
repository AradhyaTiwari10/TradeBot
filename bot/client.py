"""Binance client helper for Futures Testnet.

Provides a single function `get_client` that returns a configured
python-binance Client connected to the Binance Futures Testnet.
"""

from typing import Any
import os

from dotenv import load_dotenv
from binance.client import Client

# Load environment variables from a .env file (if present)
load_dotenv()


def get_client() -> Client:
    """Create and return a configured Binance Client for Futures Testnet.

    Raises:
        ValueError: if API_KEY or API_SECRET are not set in the environment.
    """
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        raise ValueError(
            "Missing Binance API credentials. Set API_KEY and API_SECRET in the environment."
        )

    # Use testnet=True to connect to Binance Futures Testnet
    client = Client(api_key, api_secret, testnet=True)
    return client


if __name__ == "__main__":
    # Optional quick smoke test when run directly
    client = get_client()
    print(client.futures_account_balance())
