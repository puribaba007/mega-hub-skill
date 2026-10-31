"""Time-machine backtest on intraday bars with realistic Indian costs.

Rules that keep it honest:
  * signal on bar i close -> fill at bar i+1 open (+ slippage)
  * stop is checked before target inside the same bar (worst case)
  * every position is squared off at session.square_off_at
  * all risk limits from RiskManager apply across symbols, in time order
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd

from .costs import intraday_charges, slip
from .indicators import add_intraday_indicators
from .journal import Trade, gross
from .risk import RiskManager
from .strategy import Signal, make_strategy


@dataclass
class Position:
    sig: Signal
    qty: int
    entry: float
    entry_time: datetime


def _exit_side(side: str) -> str:
    return "SELL" if side == "BUY" else "BUY"


def bar_exit(pos: Position, bar) -> tuple[float, str] | None:
    """Return (price, reason) if stop/target touched in this bar; stop wins ties."""
    s = pos.sig
    if s.side == "BUY":
        if bar["low"] <= s.stop:
            return min(s.stop, bar["open"]), "stop"
        if bar["high"] >= s.target:
            return max(s.target, bar["open"]), "target"
    else:
        if bar["high"] >= s.stop:
            return max(s.stop, bar["open"]), "stop"
        if bar["low"] <= s.target:
            return min(s.target, bar["open"]), "target"
    return None


def close_trade(pos: Position, price: float, ts: datetime, why: str, cfg, add_slippage: bool = True) -> Trade:
    """Book a closed trade. add_slippage=False when `price` is already a real broker fill."""
    s = pos.sig
    fill = slip(price, _exit_side(s.side), cfg.costs.slippage_bps) if add_slippage else price
    buy_v, sell_v = (pos.entry * pos.qty, fill * pos.qty) if s.side == "BUY" else (fill * pos.qty, pos.entry * pos.qty)
    ch = intraday_charges(buy_v, sell_v, cfg.costs).total
    g = gross(s.side, pos.qty, pos.entry, fill)
    risk_rs = abs(pos.entry - s.stop) * pos.qty
    return Trade(s.symbol, s.side, pos.qty, pos.entry_time, round(pos.entry, 2), ts, round(fill, 2), why,
                 round(g, 2), round(ch, 2), round(g - ch, 2), round((g - ch) / risk_rs, 2) if risk_rs else 0.0,
                 s.reason)


def run_backtest(data: dict[str, pd.DataFrame], cfg) -> tuple[list[Trade], pd.Series]:
    strat = make_strategy(cfg)
    risk = RiskManager(cfg, kill_dir="/nonexistent")  # kill file ignored in backtests
    prepared = {s: add_intraday_indicators(df, cfg.strategy.atr_period) for s, df in data.items() if len(df)}
    equity = float(cfg.capital)
    trades: list[Trade] = []
    curve: dict[datetime, float] = {}

    by_day: dict = {}
    for s, df in prepared.items():
        pos_idx = pd.Series(range(len(df)), index=df.index)
        for day, part in df.groupby(df.index.date):
            rows = {ts: (int(pos_idx[ts]), r) for ts, r in zip(part.index, part.to_dict("records"))}
            by_day.setdefault(day, {})[s] = rows
    for day in sorted(by_day):
        risk.new_day()
        today = by_day[day]
        stamps = sorted({ts for rows in today.values() for ts in rows})
        pending: dict[str, Signal] = {}
        open_pos: dict[str, Position] = {}
        last_bar: dict[str, tuple[datetime, dict]] = {}

        for ts in stamps:
            for sym, rows in today.items():
                if ts not in rows:
                    continue
                i, bar = rows[ts]
                last_bar[sym] = (ts, bar)
                t = ts.time()

                # 1) fill a pending signal at this bar's open
                if sym in pending:
                    sig = pending.pop(sym)
                    ok, _ = risk.can_open(t, sym, equity)
                    px = slip(bar["open"], sig.side, cfg.costs.slippage_bps)
                    gapped = (sig.side == "BUY" and px <= sig.stop) or (sig.side == "SELL" and px >= sig.stop)
                    if ok and not gapped:
                        qty = risk.position_size(equity, px, sig.stop)
                        if qty > 0:
                            # keep the planned R:R relative to the actual fill
                            r = abs(px - sig.stop)
                            sig.target = px + cfg.strategy.target_r * r if sig.side == "BUY" else px - cfg.strategy.target_r * r
                            open_pos[sym] = Position(sig, qty, px, ts)
                            risk.on_open(sym)

                # 2) manage open position
                if sym in open_pos:
                    pos = open_pos[sym]
                    hit = bar_exit(pos, bar)
                    if hit is None and risk.must_square_off(t):
                        hit = (bar["open"], "square-off")
                    if hit:
                        tr = close_trade(pos, hit[0], ts, hit[1], cfg)
                        trades.append(tr)
                        equity += tr.net_pnl
                        risk.on_close(tr.net_pnl)
                        del open_pos[sym]
                        curve[ts] = equity
                    continue

                # 3) look for a new signal on this closed bar
                if sym not in risk.day.traded_symbols and sym not in pending:
                    sig = strat.check(sym, prepared[sym], i)
                    if sig and risk.can_open(t, sym, equity)[0]:
                        pending[sym] = sig

        for sym, pos in list(open_pos.items()):  # data ended before square-off time
            ts, bar = last_bar[sym]
            tr = close_trade(pos, bar["close"], ts, "eod", cfg)
            trades.append(tr)
            equity += tr.net_pnl
            curve[ts] = equity

    return trades, pd.Series(curve, dtype=float).sort_index()


def summary(trades: list[Trade], curve: pd.Series, capital: float) -> dict:
    if not trades:
        return {"trades": 0}
    net = np.array([t.net_pnl for t in trades])
    wins, losses = net[net > 0], net[net <= 0]
    eq = pd.concat([pd.Series([capital]), curve.reset_index(drop=True)])
    dd = (eq - eq.cummax()) / eq.cummax() * 100
    return {
        "trades": len(trades),
        "win_rate_pct": round(len(wins) / len(net) * 100, 1),
        "gross_pnl_rs": round(sum(t.gross_pnl for t in trades), 2),
        "net_pnl_rs": round(net.sum(), 2),
        "return_pct": round(net.sum() / capital * 100, 2),
        "charges_rs": round(sum(t.charges for t in trades), 2),
        "avg_r": round(float(np.mean([t.r_multiple for t in trades])), 2),
        "profit_factor": round(wins.sum() / abs(losses.sum()), 2) if losses.sum() else float("inf"),
        "max_drawdown_pct": round(float(dd.min()), 2),
        "exits": pd.Series([t.exit_reason for t in trades]).value_counts().to_dict(),
    }
