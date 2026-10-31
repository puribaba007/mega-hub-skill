"""Paper broker: fills at last traded price + slippage. No money moves."""
from __future__ import annotations

import itertools

from ..costs import slip
from .base import Broker, OrderResult


class PaperBroker(Broker):
    is_live = False

    def __init__(self, feed, slippage_bps: float = 3):
        self.feed, self.bps = feed, slippage_bps
        self._ids = itertools.count(1)
        self.orders: dict[str, OrderResult] = {}

    def _new(self, status: str, price: float | None = None, msg: str = "") -> OrderResult:
        o = OrderResult(f"PAPER-{next(self._ids)}", status, price, msg)
        self.orders[o.order_id] = o
        return o

    def market(self, symbol, side, qty):
        px = self.ltp(symbol)
        if px is None:
            return self._new("REJECTED", msg="no price")
        return self._new("COMPLETE", round(slip(px, side, self.bps), 2))

    def stop_loss(self, symbol, side, qty, trigger):
        # Virtual protective stop: the engine watches LTP and exits itself in paper mode.
        return self._new("TRIGGER PENDING", msg=f"virtual SL @ {trigger}")

    def status(self, order_id):
        return self.orders[order_id]

    def cancel(self, order_id):
        o = self.orders.get(order_id)
        if o and o.status != "COMPLETE":
            o.status = "CANCELLED"

    def ltp(self, symbol):
        return self.feed.ltp(symbol)
