# 🇮🇳 India Algo Bot — personal intraday algo for NSE

Your own automated day-trading system for the **Indian stock market (NSE cash, intraday MIS)**,
built on the Mega Hub **day-trader pipeline**:

```
scanner → news filter → entry → exit → time-machine backtest → budget → risk → broker
```

> **Paper trading by default.** No real order is ever placed unless you switch to live mode
> on purpose (three separate locks, see *Going live*).

## Kya karta hai (what it does)

| Step | Module | Kaam |
|---|---|---|
| Scanner | `algobot/scanner.py` | NIFTY-50 list mein se liquid + volatile + trending stocks chunta hai (turnover, ATR %, gap, relative volume) |
| News | `algobot/news.py` | Google News headlines mein red flags (fraud, raid, SEBI order, downgrade …) wale stock skip |
| Entry | `algobot/strategy.py` | **ORB** (Opening Range Breakout + VWAP) ya **VWAP pullback** (EMA9/21 trend) |
| Exit | `strategy.py` / `engine.py` | ATR stop-loss, 2R target, 15:10 par auto square-off |
| Time machine | `algobot/backtest.py` | Past 5-min data par test — next-bar fill, slippage, asli Indian charges |
| Budget + Risk | `algobot/risk.py` | 1% risk/trade, 2% daily max loss → bot band, max 5 trades, max 3 positions, `STOP` file = kill switch |
| Charges | `algobot/costs.py` | Brokerage, STT, NSE txn, SEBI fee, stamp duty, GST |
| Broker | `algobot/brokers/` | `paper` (default) ya `zerodha` (Kite Connect) |
| Alerts | `algobot/alerts.py` | Console + optional Telegram |
| Journal | `journal/trades.csv` | Har trade ka record |

## Setup (5 minute)

```bash
cd india-algo-bot
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q tests                               # 18 tests should pass
```

## Use

```bash
python -m algobot demo                 # offline engine check on random data (no internet)
python -m algobot scan                 # today's watchlist
python -m algobot backtest             # last ~59 days of real 5-min NSE data (Yahoo, free)
python -m algobot backtest --symbols RELIANCE SBIN INFY
python -m algobot backtest --csv-dir mydata/   # your own CSVs: datetime,open,high,low,close,volume
python -m algobot run                  # paper trading loop, 09:15–15:15 IST
```

Change everything in **`config.yaml`**: capital, risk %, stocks, strategy (`orb` / `vwap_pullback`),
times, charges.

**Kill switch:** create an empty file named `STOP` inside `india-algo-bot/` — no new entries.

**Telegram alerts (optional):** `export TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=...` and set
`alerts.telegram: true`.

## Recommended path

1. `demo` → engine works.
2. `backtest` on both strategies, different stocks. Look at **net** P&L after charges,
   profit factor > 1.3, max drawdown you can live with.
3. `run` in **paper** mode for at least **2–4 weeks**. Compare paper journal with backtest.
4. Only then consider live, with small capital.

## Going live (Zerodha Kite Connect)

1. Kite Connect developer app (paid plan) → `pip install kiteconnect`.
2. Generate the daily access token after login (Kite tokens expire every day).
3. Keys only in environment variables — **never in config.yaml or git**:
   ```bash
   export KITE_API_KEY=xxxx KITE_ACCESS_TOKEN=yyyy
   ```
4. `config.yaml`: `mode: live`, `broker: zerodha`.
5. Three locks must all be open:
   ```bash
   export ALGOBOT_LIVE=YES
   python -m algobot run --i-accept-live-risk      # then type: I UNDERSTAND
   ```
   With `confirm_each_order: true` (default) you type `YES` before **every** order.

Live safety built in: every entry gets an exchange-side **SL order** (protects you even if your
PC/internet dies), the bot exits itself at target / 15:10, and alerts you to close manually if an
exit order fails.

### Regulatory note (India)
SEBI's 2025 framework for retail algo trading requires API orders to go through your broker's
registered setup (static IP registration, order-rate limits; high-frequency algos need exchange
approval). This bot is low-frequency (max 5 trades/day) and for **your own account only** —
do not sell it, share signals for money, or run it for others. Confirm the current rules with your
broker before going live. Intraday profits are taxed as speculative business income.

## Honest limits

- **No strategy is guaranteed to make money.** SEBI's own studies show most intraday traders lose.
  Backtest results do not promise future returns.
- Yahoo data is free but ~15 min delayed — fine for backtests/paper, **not** for live
  (live uses Kite data).
- Equity cash intraday only. F&O is deliberately not included.
- Update NSE holidays and charge rates in `config.yaml` every year.

Not investment advice. You are responsible for every trade.
