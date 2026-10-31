"""NSE session timing in IST."""
from __future__ import annotations

from datetime import date, datetime, time
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)


def now_ist() -> datetime:
    return datetime.now(IST)


def parse_hhmm(s: str) -> time:
    h, m = s.split(":")
    return time(int(h), int(m))


def is_trading_day(d: date, holidays: list[str]) -> bool:
    return d.weekday() < 5 and d.isoformat() not in set(holidays)


def is_market_open(ts: datetime, holidays: list[str]) -> bool:
    ts = ts.astimezone(IST)
    return is_trading_day(ts.date(), holidays) and MARKET_OPEN <= ts.time() < MARKET_CLOSE


def nse_symbol(symbol: str) -> str:
    """Yahoo Finance ticker for an NSE symbol (RELIANCE -> RELIANCE.NS)."""
    return symbol if symbol.endswith(".NS") else f"{symbol}.NS"
