"""Intraday entry rules. `check(df, i)` looks only at bars <= i (bar i just closed)."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

import pandas as pd

from .market import MARKET_OPEN


@dataclass
class Signal:
    symbol: str
    side: str          # BUY (long) or SELL (short)
    entry: float       # reference price (bar close); real fill = next bar open
    stop: float
    target: float
    time: datetime
    reason: str

    @property
    def risk_per_share(self) -> float:
        return abs(self.entry - self.stop)


def _today(df: pd.DataFrame, i: int) -> pd.DataFrame:
    """Today's bars up to and including bar i (index must be sorted)."""
    start = df.index.searchsorted(df.index[i].normalize())
    return df.iloc[start: i + 1]


def _levels(side: str, entry: float, stop: float, target_r: float) -> float:
    risk = abs(entry - stop)
    return entry + target_r * risk if side == "BUY" else entry - target_r * risk


class ORB:
    """Opening Range Breakout confirmed by VWAP."""

    def __init__(self, cfg):
        s = cfg.strategy
        self.orb_minutes, self.sl_mult, self.target_r = s.orb_minutes, s.sl_atr_mult, s.target_r
        self.allow_short = s.allow_short

    def check(self, symbol: str, df: pd.DataFrame, i: int) -> Signal | None:
        today = _today(df, i)
        ts = df.index[i]
        open_dt = ts.replace(hour=MARKET_OPEN.hour, minute=MARKET_OPEN.minute, second=0, microsecond=0)
        range_end = open_dt + timedelta(minutes=self.orb_minutes)
        rng = today[today.index < range_end]
        after = today[today.index >= range_end]
        if rng.empty or after.empty or ts < range_end:
            return None
        hi, lo = rng["high"].max(), rng["low"].min()
        row = df.iloc[i]
        prev_close = after["close"].iloc[-2] if len(after) > 1 else rng["close"].iloc[-1]
        c, a, v = row["close"], row["atr"], row["vwap"]
        if c > hi and prev_close <= hi and c > v:
            stop = max(lo, c - self.sl_mult * a)
            if stop < c:
                return Signal(symbol, "BUY", c, stop, _levels("BUY", c, stop, self.target_r), ts,
                              f"ORB breakout > {hi:.2f}, above VWAP")
        if self.allow_short and c < lo and prev_close >= lo and c < v:
            stop = min(hi, c + self.sl_mult * a)
            if stop > c:
                return Signal(symbol, "SELL", c, stop, _levels("SELL", c, stop, self.target_r), ts,
                              f"ORB breakdown < {lo:.2f}, below VWAP")
        return None


class VWAPPullback:
    """Trend (EMA9 > EMA21, price > VWAP) + pullback to EMA21 that closes back in trend."""

    def __init__(self, cfg):
        s = cfg.strategy
        self.sl_mult, self.target_r, self.allow_short = s.sl_atr_mult, s.target_r, s.allow_short

    def check(self, symbol: str, df: pd.DataFrame, i: int) -> Signal | None:
        if len(_today(df, i)) < 6:
            return None
        r = df.iloc[i]
        ts = df.index[i]
        c, a = r["close"], r["atr"]
        if r["ema9"] > r["ema21"] and c > r["vwap"] and r["low"] <= r["ema21"] < c and 45 <= r["rsi"] <= 70:
            stop = min(r["low"], c - self.sl_mult * a)
            return Signal(symbol, "BUY", c, stop, _levels("BUY", c, stop, self.target_r), ts,
                          "uptrend pullback to EMA21 above VWAP")
        if self.allow_short and r["ema9"] < r["ema21"] and c < r["vwap"] and r["high"] >= r["ema21"] > c \
                and 30 <= r["rsi"] <= 55:
            stop = max(r["high"], c + self.sl_mult * a)
            return Signal(symbol, "SELL", c, stop, _levels("SELL", c, stop, self.target_r), ts,
                          "downtrend pullback to EMA21 below VWAP")
        return None


def make_strategy(cfg):
    return {"orb": ORB, "vwap_pullback": VWAPPullback}[cfg.strategy.name](cfg)
