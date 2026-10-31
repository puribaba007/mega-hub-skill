"""Indian intraday equity (NSE cash, MIS) transaction charges."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Charges:
    brokerage: float
    stt: float
    exchange: float
    sebi: float
    stamp: float
    gst: float

    @property
    def total(self) -> float:
        return self.brokerage + self.stt + self.exchange + self.sebi + self.stamp + self.gst


def intraday_charges(buy_value: float, sell_value: float, c) -> Charges:
    """c = cfg.costs. Values are ₹ turnover of the buy leg and the sell leg."""
    def brk(v: float) -> float:
        return min(c.brokerage_flat, v * c.brokerage_pct / 100) if v > 0 else 0.0

    turnover = buy_value + sell_value
    brokerage = brk(buy_value) + brk(sell_value)
    stt = sell_value * c.stt_sell_pct / 100
    exchange = turnover * c.exchange_txn_pct / 100
    sebi = turnover * c.sebi_per_crore / 1e7
    stamp = buy_value * c.stamp_buy_pct / 100
    gst = (brokerage + exchange + sebi) * c.gst_pct / 100
    return Charges(brokerage, stt, exchange, sebi, stamp, gst)


def slip(price: float, side: str, bps: float) -> float:
    """Worse fill: pay more when buying, receive less when selling."""
    f = bps / 10_000
    return price * (1 + f) if side == "BUY" else price * (1 - f)
