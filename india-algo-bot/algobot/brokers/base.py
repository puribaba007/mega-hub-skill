from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class OrderResult:
    order_id: str
    status: str          # COMPLETE / OPEN / TRIGGER PENDING / REJECTED / CANCELLED
    avg_price: float | None = None
    message: str = ""


class Broker(ABC):
    is_live = False

    @abstractmethod
    def market(self, symbol: str, side: str, qty: int) -> OrderResult: ...

    @abstractmethod
    def stop_loss(self, symbol: str, side: str, qty: int, trigger: float) -> OrderResult: ...

    @abstractmethod
    def status(self, order_id: str) -> OrderResult: ...

    @abstractmethod
    def cancel(self, order_id: str) -> None: ...

    @abstractmethod
    def ltp(self, symbol: str) -> float | None: ...


def tick(price: float, size: float = 0.05) -> float:
    """Round to NSE tick size (₹0.05 for most cash stocks)."""
    return round(round(price / size) * size, 2)
