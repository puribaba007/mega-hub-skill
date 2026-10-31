"""Command line:  python -m algobot {demo,scan,backtest,run}"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from .alerts import Alerts
from .backtest import run_backtest, summary
from .config import load_config
from .data import load_csv_dir, synthetic_intraday
from .journal import write

ROOT = Path(__file__).resolve().parent.parent
LIVE_BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║  LIVE MODE — REAL MONEY. Orders go to your broker account.        ║
║  • Backtest + paper trade at least 2–4 weeks first.               ║
║  • Keep the broker app open; create a file named STOP to halt.    ║
║  • You are responsible for every order (SEBI rules apply).        ║
╚══════════════════════════════════════════════════════════════════╝"""


def _print_summary(trades, curve, capital, out: Path | None):
    s = summary(trades, curve, capital)
    print(json.dumps(s, indent=2, default=str))
    if out and trades:
        if out.exists():
            out.unlink()
        print(f"trades written to {write(trades, out)}")


def cmd_demo(cfg, args):
    print("Demo backtest on SYNTHETIC random-walk data (offline, not real prices).\n"
          "A random walk has no edge: expect ~0 gross P&L and a loss after charges.\n"
          "That is the point — it proves the engine has no look-ahead bias.\n")
    data = {s: synthetic_intraday(s, days=args.days, seed=i) for i, s in enumerate(cfg.universe[:5])}
    trades, curve = run_backtest(data, cfg)
    _print_summary(trades, curve, cfg.capital, ROOT / cfg.journal_dir / "demo_trades.csv")


def cmd_backtest(cfg, args):
    if args.csv_dir:
        data = load_csv_dir(args.csv_dir)
    else:
        from .data import YahooFeed
        feed = YahooFeed()
        period = f"{min(args.days, 59)}d"  # Yahoo keeps ~60 days of 5m bars
        data = {}
        for s in (args.symbols or cfg.universe):
            df = feed.intraday(s, cfg.strategy.interval, period)
            if df.empty:
                print(f"no data for {s}", file=sys.stderr)
            else:
                data[s] = df
    if not data:
        sys.exit("No data. Check internet access or pass --csv-dir.")
    trades, curve = run_backtest(data, cfg)
    _print_summary(trades, curve, cfg.capital, ROOT / cfg.journal_dir / "backtest_trades.csv")


def cmd_scan(cfg, args):
    from .data import YahooFeed
    from .scanner import scan
    feed = YahooFeed()
    picks = scan({s: feed.daily(s) for s in cfg.universe}, cfg.scanner)
    if not picks:
        print("No stocks passed the filters today.")
    for p in picks:
        print(f"{p.symbol:12s} {p.bias:5s} score {p.score:5.2f}  ₹{p.close:>9,.2f}  ATR {p.atr_pct}%  "
              f"gap {p.gap_pct:+.2f}%  relVol {p.rel_volume}x  turnover ₹{p.turnover_cr} cr")


def cmd_run(cfg, args):
    from .brokers import make_broker
    from .engine import Engine
    if cfg.mode == "live":
        print(LIVE_BANNER)
        if os.getenv("ALGOBOT_LIVE") != "YES" or not args.i_accept_live_risk:
            sys.exit("Refusing live mode: set env ALGOBOT_LIVE=YES and pass --i-accept-live-risk.")
        if input("Type 'I UNDERSTAND' to start live trading: ").strip() != "I UNDERSTAND":
            sys.exit("Cancelled.")
    if cfg.broker == "zerodha":
        from .brokers.zerodha import KiteFeed, ZerodhaBroker
        broker = ZerodhaBroker()
        feed = KiteFeed(broker)
    else:
        from .data import YahooFeed
        feed = YahooFeed()
        broker = make_broker(cfg, feed)
    if cfg.mode == "paper" and broker.is_live:
        sys.exit("mode: paper with a live broker is not allowed — set broker: paper.")
    Engine(cfg, feed, broker, Alerts(cfg.alerts.telegram), ROOT).run()


def main(argv=None):
    p = argparse.ArgumentParser(prog="algobot", description="Personal NSE intraday algo bot (paper-first)")
    p.add_argument("--config", default=str(ROOT / "config.yaml"))
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("demo", help="offline backtest on synthetic data")
    d.add_argument("--days", type=int, default=30)
    b = sub.add_parser("backtest", help="backtest on Yahoo 5m data or your CSVs")
    b.add_argument("--days", type=int, default=59)
    b.add_argument("--symbols", nargs="*")
    b.add_argument("--csv-dir")
    sub.add_parser("scan", help="today's watchlist from the scanner")
    r = sub.add_parser("run", help="run the trading loop (paper or live per config)")
    r.add_argument("--i-accept-live-risk", action="store_true")
    a = p.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    cfg = load_config(a.config)
    {"demo": cmd_demo, "backtest": cmd_backtest, "scan": cmd_scan, "run": cmd_run}[a.cmd](cfg, a)
