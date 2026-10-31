from datetime import datetime, time

import numpy as np
import pandas as pd
import pytest

from algobot.backtest import Position, bar_exit, run_backtest, summary
from algobot.config import validate
from algobot.costs import intraday_charges
from algobot.data import synthetic_intraday
from algobot.indicators import add_intraday_indicators, ema, vwap
from algobot.market import IST, is_market_open
from algobot.risk import RiskManager
from algobot.strategy import ORB, Signal


def day_bars(prices, day="2026-10-29", vol=100_000):
    idx = pd.date_range(f"{day} 09:15", periods=len(prices), freq="5min", tz=IST)
    p = np.array(prices, float)
    o = np.concatenate([[p[0]], p[:-1]])
    return pd.DataFrame({"open": o, "high": np.maximum(o, p) + 0.5, "low": np.minimum(o, p) - 0.5,
                         "close": p, "volume": vol}, index=idx)


# ---------- indicators ----------
def test_ema_matches_pandas():
    s = pd.Series(np.arange(50, dtype=float))
    assert np.allclose(ema(s, 9), s.ewm(span=9, adjust=False).mean())


def test_vwap_resets_each_day():
    df = pd.concat([day_bars([100] * 5, "2026-10-28"), day_bars([200] * 5, "2026-10-29")])
    v = vwap(df)
    assert v.iloc[4] == pytest.approx(100)
    assert v.iloc[5] == pytest.approx(200)  # first bar of new day ignores yesterday


def test_indicators_are_causal():
    df = synthetic_intraday("X", days=3, seed=1)
    full = add_intraday_indicators(df)
    part = add_intraday_indicators(df.iloc[:100])
    cols = ["ema9", "ema21", "rsi", "atr", "vwap"]
    assert np.allclose(full[cols].iloc[:100].values, part[cols].values)


# ---------- costs ----------
def test_intraday_charges_known_values(cfg):
    ch = intraday_charges(100_000, 101_000, cfg.costs)
    assert ch.brokerage == pytest.approx(40)            # ₹20 cap per side
    assert ch.stt == pytest.approx(25.25)               # 0.025% of sell
    assert ch.stamp == pytest.approx(3.0)               # 0.003% of buy
    assert ch.exchange == pytest.approx(201_000 * 0.00297 / 100)
    assert ch.gst == pytest.approx((ch.brokerage + ch.exchange + ch.sebi) * 0.18)


def test_small_order_brokerage_is_percent(cfg):
    assert intraday_charges(10_000, 10_000, cfg.costs).brokerage == pytest.approx(6)  # 0.03% × 2


# ---------- risk ----------
def test_position_size_respects_risk_and_exposure(cfg):
    r = RiskManager(cfg, kill_dir="/nonexistent")
    assert r.position_size(100_000, 1000, 990) == 30  # exposure cap 30% → 30 shares (risk allows 100)
    assert r.position_size(100_000, 100, 90) == 100   # risk cap: ₹1000 / ₹10
    assert r.position_size(100_000, 100, 100) == 0


def test_risk_limits(cfg, tmp_path):
    r = RiskManager(cfg, kill_dir=tmp_path)
    assert r.can_open(time(9, 20), "A", 1e5)[0] is False      # before start_after
    assert r.can_open(time(14, 50), "A", 1e5)[0] is False     # after last entry
    assert r.can_open(time(10, 0), "A", 1e5)[0] is True
    r.on_open("A")
    assert r.can_open(time(10, 0), "A", 1e5)[0] is False      # one trade per symbol per day
    r.on_close(-2500)
    ok, why = r.can_open(time(10, 0), "B", 1e5)
    assert not ok and "daily loss" in why
    r.new_day()
    (tmp_path / "STOP").write_text("")
    assert r.can_open(time(10, 0), "B", 1e5) == (False, "kill switch file STOP present")


def test_live_config_guards(cfg):
    cfg.mode, cfg.broker = "live", "paper"
    with pytest.raises(ValueError):
        validate(cfg)
    cfg.mode, cfg.risk.risk_per_trade_pct = "paper", 10
    with pytest.raises(ValueError):
        validate(cfg)


def test_market_hours():
    assert is_market_open(datetime(2026, 10, 29, 10, 0, tzinfo=IST), [])
    assert not is_market_open(datetime(2026, 10, 31, 10, 0, tzinfo=IST), [])          # Saturday
    assert not is_market_open(datetime(2026, 10, 29, 15, 30, tzinfo=IST), [])
    assert not is_market_open(datetime(2026, 10, 2, 10, 0, tzinfo=IST), ["2026-10-02"])


# ---------- strategy ----------
def test_orb_long_breakout(cfg):
    prices = [100, 101, 100.5] + [100.8, 101.2, 102.5]  # range 09:15-09:30, break at 09:40 bar
    df = add_intraday_indicators(day_bars(prices))
    orb = ORB(cfg)
    assert orb.check("X", df, 2) is None              # still inside opening range
    sig = orb.check("X", df, 5)
    assert sig and sig.side == "BUY" and sig.stop < sig.entry < sig.target
    assert sig.target - sig.entry == pytest.approx(cfg.strategy.target_r * (sig.entry - sig.stop))


def test_orb_no_signal_inside_range(cfg):
    df = add_intraday_indicators(day_bars([100, 101, 99, 100, 100.2, 100.4]))
    assert all(ORB(cfg).check("X", df, i) is None for i in range(len(df)))


def test_stop_wins_when_bar_hits_both():
    sig = Signal("X", "BUY", 100, 98, 104, datetime.now(IST), "")
    pos = Position(sig, 10, 100, datetime.now(IST))
    assert bar_exit(pos, {"open": 100, "high": 105, "low": 97}) == (98, "stop")
    assert bar_exit(pos, {"open": 95, "high": 96, "low": 94}) == (95, "stop")  # gap below stop
    assert bar_exit(pos, {"open": 101, "high": 104.5, "low": 99}) == (104, "target")


# ---------- backtest ----------
def test_backtest_fills_next_bar_and_squares_off(cfg):
    data = {s: synthetic_intraday(s, days=15, seed=i) for i, s in enumerate(["A", "B", "C"])}
    trades, curve = run_backtest(data, cfg)
    assert trades
    sq = time(15, 10)
    for t in trades:
        assert t.entry_time.time() >= time(9, 30)
        assert t.exit_time.time() <= sq
        assert t.entry_time.date() == t.exit_time.date()          # intraday only
        assert t.net_pnl == pytest.approx(t.gross_pnl - t.charges, abs=0.02)
    per_day = pd.Series([t.entry_time.date() for t in trades]).value_counts()
    assert per_day.max() <= cfg.risk.max_trades_per_day
    s = summary(trades, curve, cfg.capital)
    assert s["trades"] == len(trades)


def test_random_walk_has_no_edge(cfg):
    """Look-ahead guard: on pure noise, gross P&L per trade should be ~0 R."""
    data = {s: synthetic_intraday(s, days=60, seed=10 + i) for i, s in enumerate("ABCDE")}
    trades, _ = run_backtest(data, cfg)
    avg_gross = np.mean([t.gross_pnl for t in trades])
    risk_rs = cfg.capital * cfg.risk.risk_per_trade_pct / 100
    assert len(trades) > 100
    assert abs(avg_gross) < 0.25 * risk_rs, avg_gross
