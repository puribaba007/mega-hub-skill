"""Position sizing + daily guard-rails. Every entry must pass `can_open`."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import time
from pathlib import Path

from .market import parse_hhmm

KILL_FILE = "STOP"  # create a file named STOP next to config.yaml to halt new entries


@dataclass
class DayState:
    trades: int = 0
    realized_pnl: float = 0.0
    open_positions: int = 0
    halted: bool = False
    halt_reason: str = ""
    traded_symbols: set = field(default_factory=set)


class RiskManager:
    def __init__(self, cfg, kill_dir: str | Path = "."):
        self.r = cfg.risk
        self.start_after: time = parse_hhmm(cfg.session.start_after)
        self.last_entry: time = parse_hhmm(cfg.session.no_new_entries_after)
        self.square_off: time = parse_hhmm(cfg.session.square_off_at)
        self.kill_path = Path(kill_dir) / KILL_FILE
        self.day = DayState()

    def new_day(self) -> None:
        self.day = DayState()

    def position_size(self, equity: float, entry: float, stop: float) -> int:
        per_share_risk = abs(entry - stop)
        if per_share_risk <= 0 or entry <= 0:
            return 0
        by_risk = equity * self.r.risk_per_trade_pct / 100 / per_share_risk
        by_exposure = equity * self.r.leverage * self.r.max_position_pct / 100 / entry
        return max(0, math.floor(min(by_risk, by_exposure)))

    def can_open(self, t: time, symbol: str, equity: float) -> tuple[bool, str]:
        d = self.day
        if self.kill_path.exists():
            return False, "kill switch file STOP present"
        if d.halted:
            return False, d.halt_reason
        if d.realized_pnl <= -equity * self.r.max_daily_loss_pct / 100:
            d.halted, d.halt_reason = True, "max daily loss hit — done for today"
            return False, d.halt_reason
        if t < self.start_after or t >= self.last_entry:
            return False, "outside entry window"
        if d.trades >= self.r.max_trades_per_day:
            return False, "max trades per day reached"
        if d.open_positions >= self.r.max_open_positions:
            return False, "max open positions reached"
        if symbol in d.traded_symbols:
            return False, "already traded this symbol today"
        return True, "ok"

    def on_open(self, symbol: str) -> None:
        self.day.trades += 1
        self.day.open_positions += 1
        self.day.traded_symbols.add(symbol)

    def on_close(self, net_pnl: float) -> None:
        self.day.open_positions = max(0, self.day.open_positions - 1)
        self.day.realized_pnl += net_pnl

    def must_square_off(self, t: time) -> bool:
        return t >= self.square_off
