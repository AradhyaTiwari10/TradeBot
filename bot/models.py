"""Data models for trading requests and responses.

Uses dataclasses for lightweight, typed structures shared across modules.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderRequest:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None


@dataclass
class OrderResponse:
    order_id: int
    status: str
    executed_qty: float
    avg_price: Optional[float] = None
