"""Pre-market scanner: liquid, volatile, trending NSE stocks worth watching today."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .indicators import atr, ema


@dataclass
class Pick:
    symbol: str
    score: float
    bias: str            # LONG / SHORT
    close: float
    atr_pct: float
    turnover_cr: float
    gap_pct: float
    rel_volume: float


def score_symbol(symbol: str, daily: pd.DataFrame, sc) -> Pick | None:
    if daily is None or len(daily) < 25:
        return None
    d = daily.copy()
    d["atr"] = atr(d, 14)
    d["ema20"] = ema(d["close"], 20)
    last, prev = d.iloc[-1], d.iloc[-2]
    close = float(last["close"])
    turnover_cr = float((d["close"] * d["volume"]).tail(20).mean() / 1e7)
    atr_pct = float(last["atr"] / close * 100)
    if not (sc.min_price <= close <= sc.max_price):
        return None
    if turnover_cr < sc.min_avg_turnover_cr or atr_pct < sc.min_atr_pct:
        return None
    gap_pct = float((last["open"] - prev["close"]) / prev["close"] * 100)
    rel_vol = float(last["volume"] / d["volume"].tail(21).head(20).mean())
    trend = (close - float(last["ema20"])) / close * 100
    bias = "LONG" if trend >= 0 else "SHORT"
    score = atr_pct + min(rel_vol, 4) + abs(gap_pct) * 0.5 + min(abs(trend), 5) * 0.3
    return Pick(symbol, round(score, 2), bias, round(close, 2), round(atr_pct, 2),
                round(turnover_cr, 1), round(gap_pct, 2), round(rel_vol, 2))


def scan(dailies: dict[str, pd.DataFrame], sc) -> list[Pick]:
    picks = [p for s, df in dailies.items() if (p := score_symbol(s, df, sc))]
    return sorted(picks, key=lambda p: p.score, reverse=True)[: sc.top_n]
