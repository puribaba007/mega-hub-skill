"""Causal indicators (value at bar i uses bars <= i only) — no look-ahead."""
from __future__ import annotations

import numpy as np
import pandas as pd


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(100.0)


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    prev = df["close"].shift()
    tr = pd.concat(
        [df["high"] - df["low"], (df["high"] - prev).abs(), (df["low"] - prev).abs()], axis=1
    ).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def vwap(df: pd.DataFrame) -> pd.Series:
    """Intraday VWAP that resets every trading day."""
    tp = (df["high"] + df["low"] + df["close"]) / 3
    day = df.index.date
    pv = (tp * df["volume"]).groupby(day).cumsum()
    vol = df["volume"].groupby(day).cumsum().replace(0, np.nan)
    return (pv / vol).fillna(tp)


def add_intraday_indicators(df: pd.DataFrame, atr_period: int = 14) -> pd.DataFrame:
    out = df.copy()
    out["ema9"] = ema(out["close"], 9)
    out["ema21"] = ema(out["close"], 21)
    out["rsi"] = rsi(out["close"], 14)
    out["atr"] = atr(out, atr_period)
    out["vwap"] = vwap(out)
    return out
