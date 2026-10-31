---
name: india-algo-trader
description: Personal automated intraday algo trading bot for the Indian stock market (NSE cash, MIS) — scanner, news filter, ORB / VWAP-pullback entries, ATR stops, backtest with real Indian charges (STT, stamp, GST), risk limits, paper trading and optional Zerodha Kite Connect live mode. Use when the user asks for an Indian market / NSE / NIFTY algo, trading bot, day-trading automation, intraday strategy backtest, or says "algo system for India", "Zerodha bot", "share market bot".
---

# India Algo Trader

Runs the Mega Hub **day-trader pipeline** on Indian markets using the code in `india-algo-bot/`.
Reply in the user's language (Hindi / Hinglish if they write that way).

## Pipeline → command

| Day-trader step | What to run (inside `india-algo-bot/`) |
|---|---|
| trader-scanner | `python -m algobot scan` |
| trader-news | built into `run` (`news.enabled`), red-flag headlines skip a stock |
| trader-entry / trader-exit | `strategy.name: orb` or `vwap_pullback` in `config.yaml`; ATR stop, `target_r` target, 15:10 square-off |
| trader-timemachine | `python -m algobot backtest [--symbols ...] [--csv-dir ...]`; offline: `python -m algobot demo` |
| trader-budget / trader-risk | `risk:` block in `config.yaml` (1% per trade, 2% daily stop, max trades/positions); `STOP` file = kill switch |
| trader-broker | `python -m algobot run` — paper by default; Zerodha only via the live locks |
| trader-alerts | Telegram via env `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| trader-analyst | read `journal/*.csv`, use `dataviz` / `anthropic-skills:xlsx` for reports |

## Rules

1. **Paper first.** Never switch `mode: live` for the user; they must do it themselves and pass all
   three locks (`ALGOBOT_LIVE=YES`, `--i-accept-live-risk`, typed confirmation).
2. Never ask for or store API keys/tokens in chat or files; env vars only.
3. Always report **net** P&L after charges, drawdown and trade count — never just win rate.
4. If a strategy change is proposed, backtest before and after and show both.
5. Mention honestly: no guaranteed profit, most intraday traders lose, SEBI retail-algo rules apply,
   personal use only. Not investment advice.
6. Before changing code, run `python -m pytest -q tests` and keep it green.
