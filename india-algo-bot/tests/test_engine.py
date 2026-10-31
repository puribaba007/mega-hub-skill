"""Engine step() with a fake feed: paper fills, stop/target handling, square-off."""
from datetime import datetime

import pandas as pd

from algobot.alerts import Alerts
from algobot.brokers import PaperBroker
from algobot.engine import Engine
from algobot.market import IST


class FakeFeed:
    def __init__(self, bars: pd.DataFrame):
        self.bars, self.price = bars, None

    def intraday(self, symbol, interval="5m", period="5d"):
        return self.bars

    def ltp(self, symbol):
        return self.price


def breakout_bars():
    # 2 warm-up days of flat bars, then today: tight range then breakout
    days = []
    for d in ["2026-10-27", "2026-10-28"]:
        idx = pd.date_range(f"{d} 09:15", periods=75, freq="5min", tz=IST)
        days.append(pd.DataFrame({"open": 100.0, "high": 100.5, "low": 99.5, "close": 100.0,
                                  "volume": 50_000}, index=idx))
    closes = [100, 100.2, 99.9, 100.1, 100.3, 101.5]
    idx = pd.date_range("2026-10-29 09:15", periods=len(closes), freq="5min", tz=IST)
    o = [100] + closes[:-1]
    days.append(pd.DataFrame({"open": o, "high": [max(a, b) + 0.2 for a, b in zip(o, closes)],
                              "low": [min(a, b) - 0.2 for a, b in zip(o, closes)], "close": closes,
                              "volume": 80_000}, index=idx))
    return pd.concat(days)


def make_engine(cfg, tmp_path, feed):
    eng = Engine(cfg, feed, PaperBroker(feed, 0), Alerts(False), tmp_path)
    eng.watchlist = ["TEST"]
    return eng


def test_paper_entry_then_target(cfg, tmp_path):
    feed = FakeFeed(breakout_bars())
    eng = make_engine(cfg, tmp_path, feed)
    feed.price = 101.6
    eng.step(datetime(2026, 10, 29, 9, 45, 5, tzinfo=IST))   # 09:40 bar closed → breakout
    assert "TEST" in eng.positions
    pos = eng.positions["TEST"]
    assert pos.sig.side == "BUY" and pos.entry == 101.6
    feed.price = pos.sig.target + 0.1
    eng.step(datetime(2026, 10, 29, 9, 50, tzinfo=IST))
    assert "TEST" not in eng.positions
    assert eng.risk.day.realized_pnl > 0
    assert (tmp_path / cfg.journal_dir / "trades.csv").exists()


def test_paper_stop_and_no_reentry(cfg, tmp_path):
    feed = FakeFeed(breakout_bars())
    eng = make_engine(cfg, tmp_path, feed)
    feed.price = 101.6
    eng.step(datetime(2026, 10, 29, 9, 45, 5, tzinfo=IST))
    feed.price = eng.positions["TEST"].sig.stop - 0.05
    eng.step(datetime(2026, 10, 29, 9, 46, tzinfo=IST))
    assert not eng.positions and eng.risk.day.realized_pnl < 0
    feed.price = 101.6
    eng.step(datetime(2026, 10, 29, 9, 50, 5, tzinfo=IST))
    assert not eng.positions  # same symbol not traded twice in a day


def test_square_off(cfg, tmp_path):
    feed = FakeFeed(breakout_bars())
    eng = make_engine(cfg, tmp_path, feed)
    feed.price = 101.6
    eng.step(datetime(2026, 10, 29, 9, 45, 5, tzinfo=IST))
    eng.step(datetime(2026, 10, 29, 15, 10, tzinfo=IST))
    assert not eng.positions


def test_forming_bar_is_ignored(cfg, tmp_path):
    feed = FakeFeed(breakout_bars())
    eng = make_engine(cfg, tmp_path, feed)
    feed.price = 101.6
    eng.step(datetime(2026, 10, 29, 9, 44, tzinfo=IST))  # 09:40 bar still forming
    assert not eng.positions
