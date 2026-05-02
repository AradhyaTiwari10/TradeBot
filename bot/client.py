"""Binance Futures Testnet client initialization."""
import os

from dotenv import load_dotenv
from binance.client import Client

load_dotenv()


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


if __name__ == "__main__":
    client = get_client()
    print(client.futures_account_balance())
