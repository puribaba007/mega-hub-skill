"""Market data: free Yahoo Finance (delayed) feed, CSV loader, synthetic demo data."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .market import IST, MARKET_CLOSE, MARKET_OPEN, nse_symbol

COLS = ["open", "high", "low", "close", "volume"]


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=COLS)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns=str.lower)[COLS].dropna()
    idx = df.index
    df.index = idx.tz_localize(IST) if idx.tz is None else idx.tz_convert(IST)
    return df


def _session_only(df: pd.DataFrame) -> pd.DataFrame:
    t = df.index.time
    return df[(t >= MARKET_OPEN) & (t < MARKET_CLOSE)]


class YahooFeed:
    """Free, ~15-min-delayed NSE data. Good for scanning, backtests and paper trading."""

    def __init__(self):
        import yfinance  # noqa: F401  (fail early with a clear error)

    def daily(self, symbol: str, period: str = "3mo") -> pd.DataFrame:
        import yfinance as yf
        df = yf.download(nse_symbol(symbol), period=period, interval="1d", progress=False, auto_adjust=False)
        return _clean(df)

    def intraday(self, symbol: str, interval: str = "5m", period: str = "5d") -> pd.DataFrame:
        import yfinance as yf
        df = yf.download(nse_symbol(symbol), period=period, interval=interval, progress=False, auto_adjust=False)
        return _session_only(_clean(df))

    def ltp(self, symbol: str) -> float | None:
        df = self.intraday(symbol, "1m", "1d")
        return float(df["close"].iloc[-1]) if not df.empty else None


def load_csv_dir(path: str | Path) -> dict[str, pd.DataFrame]:
    """Load <SYMBOL>.csv files with columns datetime,open,high,low,close,volume (IST)."""
    out = {}
    for f in sorted(Path(path).glob("*.csv")):
        df = pd.read_csv(f, parse_dates=[0], index_col=0)
        out[f.stem.upper()] = _session_only(_clean(df))
    return out


def synthetic_intraday(symbol: str, days: int = 20, start_price: float = 1000.0,
                       interval_min: int = 5, seed: int | None = None) -> pd.DataFrame:
    """Pure random-walk NSE-session bars for offline demos and tests (NOT real market data).

    There is no edge in a random walk, so a correct backtest should show ~zero gross P&L
    and a loss after costs. Use it to check the engine has no look-ahead bias."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(end=pd.Timestamp("2026-10-30"), periods=days)
    frames, price = [], start_price
    for d in dates:
        idx = pd.date_range(pd.Timestamp(d.date()).tz_localize(IST) + pd.Timedelta(hours=9, minutes=15),
                            periods=int(375 / interval_min), freq=f"{interval_min}min")
        rets = rng.normal(0, 0.0025, len(idx))
        price *= 1 + rng.normal(0, 0.008)  # overnight gap
        closes = price * np.cumprod(1 + rets)
        opens = np.concatenate([[price], closes[:-1]])
        spread = np.abs(rng.normal(0, 0.0012, len(idx))) * closes
        highs = np.maximum(opens, closes) + spread
        lows = np.minimum(opens, closes) - spread
        vol = rng.integers(20_000, 200_000, len(idx))
        frames.append(pd.DataFrame({"open": opens, "high": highs, "low": lows, "close": closes,
                                    "volume": vol}, index=idx))
        price = closes[-1]
    return pd.concat(frames)
