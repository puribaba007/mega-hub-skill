"""Live / paper trading loop. Same strategy + risk rules as the backtest."""
from __future__ import annotations

import logging
import time as _time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable

import pandas as pd

from . import news
from .backtest import Position, close_trade
from .indicators import add_intraday_indicators
from .journal import write
from .market import IST, MARKET_CLOSE, MARKET_OPEN, is_trading_day, now_ist
from .risk import RiskManager
from .scanner import scan
from .strategy import make_strategy

log = logging.getLogger("algobot")


@dataclass
class LivePosition(Position):
    sl_order_id: str = ""


class Engine:
    def __init__(self, cfg, feed, broker, alerts, root: Path,
                 confirm: Callable[[str], bool] | None = None):
        self.cfg, self.feed, self.broker, self.alerts = cfg, feed, broker, alerts
        self.strat = make_strategy(cfg)
        self.risk = RiskManager(cfg, kill_dir=root)
        self.equity = float(cfg.capital)
        self.watchlist: list[str] = []
        self.positions: dict[str, LivePosition] = {}
        self.last_bar_seen: dict[str, pd.Timestamp] = {}
        self.bar_minutes = int(cfg.strategy.interval.rstrip("m"))
        self.journal = root / cfg.journal_dir / "trades.csv"
        self.confirm = confirm or (lambda msg: input(f"{msg}  Type YES to send: ").strip() == "YES")

    # ---------- pre-market ----------
    def prepare_day(self) -> list[str]:
        self.risk.new_day()
        dailies = {}
        for s in self.cfg.universe:
            try:
                dailies[s] = self.feed.daily(s)
            except Exception as e:
                log.warning("daily data failed for %s: %s", s, e)
        picks = scan(dailies, self.cfg.scanner)
        syms = [p.symbol for p in picks]
        if self.cfg.news.enabled and syms:
            flagged = news.screen(syms, self.cfg.news.red_flags)
            for s, hits in flagged.items():
                self.alerts.send(f"⚠️ skip {s}: {hits[0]}")
            syms = [s for s in syms if s not in flagged]
        self.watchlist = syms
        self.alerts.send("📋 Watchlist: " + (", ".join(
            f"{p.symbol}({p.bias}, ATR {p.atr_pct}%)" for p in picks if p.symbol in syms) or "none"))
        return syms

    # ---------- one tick ----------
    def step(self, now: datetime) -> None:
        t = now.time()
        self._manage(now)
        if not self.risk.must_square_off(t):
            self._look_for_entries(now)

    def _completed_bars(self, sym: str, now: datetime) -> pd.DataFrame:
        df = self.feed.intraday(sym, self.cfg.strategy.interval, "5d")
        if df.empty:
            return df
        end = df.index + pd.Timedelta(minutes=self.bar_minutes)
        return df[end <= now]  # drop the still-forming bar

    def _look_for_entries(self, now: datetime) -> None:
        for sym in self.watchlist:
            if sym in self.positions or sym in self.risk.day.traded_symbols:
                continue
            ok, why = self.risk.can_open(now.time(), sym, self.equity)
            if not ok:
                if why in ("max daily loss hit — done for today", "kill switch file STOP present"):
                    return
                continue
            df = self._completed_bars(sym, now)
            if len(df) < 20 or df.index[-1].date() != now.date():
                continue
            if self.last_bar_seen.get(sym) == df.index[-1]:
                continue
            self.last_bar_seen[sym] = df.index[-1]
            df = add_intraday_indicators(df, self.cfg.strategy.atr_period)
            sig = self.strat.check(sym, df, len(df) - 1)
            if sig:
                self._enter(sig, now)

    def _enter(self, sig, now: datetime) -> None:
        px = self.broker.ltp(sig.symbol) or sig.entry
        qty = self.risk.position_size(self.equity, px, sig.stop)
        if qty <= 0:
            return
        msg = (f"{'🟢 BUY' if sig.side == 'BUY' else '🔴 SELL'} {sig.symbol} x{qty} @~{px:.2f} "
               f"SL {sig.stop:.2f} TGT {sig.target:.2f} — {sig.reason}")
        if self.broker.is_live and self.cfg.risk.confirm_each_order and not self.confirm(msg):
            self.alerts.send(f"⏭️ skipped by you: {sig.symbol}")
            self.risk.day.traded_symbols.add(sig.symbol)
            return
        res = self.broker.market(sig.symbol, sig.side, qty)
        if res.status != "COMPLETE" or not res.avg_price:
            self.alerts.send(f"❌ order failed {sig.symbol}: {res.status} {res.message}")
            self.risk.day.traded_symbols.add(sig.symbol)
            return
        fill = float(res.avg_price)
        risk_ps = abs(fill - sig.stop)
        if (sig.side == "BUY" and fill <= sig.stop) or (sig.side == "SELL" and fill >= sig.stop):
            risk_ps = abs(sig.entry - sig.stop)
            sig.stop = fill - risk_ps if sig.side == "BUY" else fill + risk_ps
        r = self.cfg.strategy.target_r
        sig.target = fill + r * risk_ps if sig.side == "BUY" else fill - r * risk_ps
        exit_side = "SELL" if sig.side == "BUY" else "BUY"
        sl = self.broker.stop_loss(sig.symbol, exit_side, qty, sig.stop)
        if sl.status == "REJECTED":
            self.alerts.send(f"🚨 SL order rejected for {sig.symbol} — exiting now for safety")
        self.positions[sig.symbol] = LivePosition(sig, qty, fill, now, sl.order_id)
        self.risk.on_open(sig.symbol)
        self.alerts.send(msg.replace(f"@~{px:.2f}", f"filled @ {fill:.2f}"))
        if sl.status == "REJECTED":
            self._exit(sig.symbol, now, "sl-rejected")

    def _manage(self, now: datetime) -> None:
        for sym, pos in list(self.positions.items()):
            if pos.sl_order_id:
                st = self.broker.status(pos.sl_order_id)
                if st.status == "COMPLETE":  # exchange stop already filled (live)
                    self._book(sym, st.avg_price or pos.sig.stop, now, "stop (exchange)", slipped=bool(st.avg_price))
                    continue
            px = self.broker.ltp(sym)
            if px is None:
                continue
            s = pos.sig
            if (s.side == "BUY" and px <= s.stop) or (s.side == "SELL" and px >= s.stop):
                self._exit(sym, now, "stop")
            elif (s.side == "BUY" and px >= s.target) or (s.side == "SELL" and px <= s.target):
                self._exit(sym, now, "target")
            elif self.risk.must_square_off(now.time()):
                self._exit(sym, now, "square-off")

    def _exit(self, sym: str, now: datetime, why: str) -> None:
        pos = self.positions[sym]
        if pos.sl_order_id:
            self.broker.cancel(pos.sl_order_id)
            st = self.broker.status(pos.sl_order_id)
            if st.status == "COMPLETE":
                self._book(sym, st.avg_price or pos.sig.stop, now, "stop (exchange)", slipped=bool(st.avg_price))
                return
        side = "SELL" if pos.sig.side == "BUY" else "BUY"
        res = self.broker.market(sym, side, pos.qty)
        if res.status != "COMPLETE":
            self.alerts.send(f"🚨 EXIT FAILED {sym} ({res.message}) — close it manually in your broker app NOW")
            return
        self._book(sym, float(res.avg_price), now, why, slipped=True)

    def _book(self, sym: str, price: float, now: datetime, why: str, slipped: bool = False) -> None:
        pos = self.positions.pop(sym)
        # a broker fill already includes slippage; only model it for stop-level estimates
        tr = close_trade(pos, price, now, why, self.cfg, add_slippage=not slipped)
        self.equity += tr.net_pnl
        self.risk.on_close(tr.net_pnl)
        write([tr], self.journal)
        self.alerts.send(f"{'✅' if tr.net_pnl > 0 else '🔻'} closed {sym} ({why}) net ₹{tr.net_pnl:,.0f} "
                         f"| day ₹{self.risk.day.realized_pnl:,.0f}")

    # ---------- main loop ----------
    def run(self, poll_seconds: int = 15, clock: Callable[[], datetime] = now_ist,
            sleep: Callable[[float], None] = _time.sleep) -> None:
        now = clock()
        if not is_trading_day(now.date(), self.cfg.holidays):
            self.alerts.send("Market closed today (weekend/holiday).")
            return
        self.prepare_day()
        if not self.watchlist:
            self.alerts.send("No stocks passed the scanner — no trades today.")
            return
        open_dt = datetime.combine(now.date(), MARKET_OPEN, IST)
        if now < open_dt:
            sleep((open_dt - now).total_seconds())
        stop_at = datetime.combine(now.date(), self.risk.square_off, IST) + timedelta(minutes=5)
        while True:
            now = clock()
            if now >= stop_at or now.time() >= MARKET_CLOSE:
                break
            try:
                self.step(now)
            except Exception as e:  # keep running; positions still have exchange SL in live mode
                log.exception("step failed: %s", e)
            sleep(poll_seconds)
        for sym in list(self.positions):
            self._exit(sym, clock(), "end-of-day")
        d = self.risk.day
        self.alerts.send(f"📊 Day done: {d.trades} trades, net ₹{d.realized_pnl:,.0f}, equity ₹{self.equity:,.0f}")
