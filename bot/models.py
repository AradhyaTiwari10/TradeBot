"""Domain models for order requests and responses."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderRequest:
    """Request model for placing an order."""
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None


@dataclass
class OrderResponse:
    """Response model from order execution."""
    order_id: int
    status: str
    executed_qty: float
    avg_price: Optional[float] = None
