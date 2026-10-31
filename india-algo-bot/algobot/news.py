"""Headline red-flag filter (Google News RSS). Network failure = no flag, never a crash."""
from __future__ import annotations

import urllib.parse
import xml.etree.ElementTree as ET

import requests


def headlines(symbol: str, limit: int = 15) -> list[str]:
    q = urllib.parse.quote(f"{symbol} NSE share when:1d")
    url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        return [i.findtext("title", "") for i in root.iter("item")][:limit]
    except Exception:
        return []


def red_flags(titles: list[str], words: list[str]) -> list[str]:
    low = [w.lower() for w in words]
    return [t for t in titles if any(w in t.lower() for w in low)]


def screen(symbols: list[str], words: list[str]) -> dict[str, list[str]]:
    """Return {symbol: [flagged headlines]} for symbols that should be skipped today."""
    out = {}
    for s in symbols:
        hits = red_flags(headlines(s), words)
        if hits:
            out[s] = hits
    return out
