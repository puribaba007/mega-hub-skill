"""Append-only CSV trade journal."""
from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Trade:
    symbol: str
    side: str
    qty: int
    entry_time: datetime
    entry: float
    exit_time: datetime
    exit: float
    exit_reason: str
    gross_pnl: float
    charges: float
    net_pnl: float
    r_multiple: float
    reason: str


def gross(side: str, qty: int, entry: float, exit_: float) -> float:
    return (exit_ - entry) * qty if side == "BUY" else (entry - exit_) * qty


def write(trades: list[Trade], path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(Trade.__dataclass_fields__))
        if new:
            w.writeheader()
        for t in trades:
            w.writerow(asdict(t))
    return path
