"""Zerodha Kite Connect adapter (live money). Needs: pip install kiteconnect

Keys come ONLY from environment variables (never commit them):
    KITE_API_KEY       — from https://developers.kite.trade
    KITE_ACCESS_TOKEN  — generate daily after login (see README "Going live")
"""
from __future__ import annotations

import os
import time

from .base import Broker, OrderResult, tick

TAG = "algobot"


class ZerodhaBroker(Broker):
    is_live = True

    def __init__(self):
        try:
            from kiteconnect import KiteConnect
        except ImportError as e:
            raise SystemExit("pip install kiteconnect  (needed for broker: zerodha)") from e
        key, token = os.getenv("KITE_API_KEY"), os.getenv("KITE_ACCESS_TOKEN")
        if not key or not token:
            raise SystemExit("Set KITE_API_KEY and KITE_ACCESS_TOKEN environment variables.")
        self.kite = KiteConnect(api_key=key)
        self.kite.set_access_token(token)

    def _place(self, **kw) -> str:
        k = self.kite
        return str(k.place_order(variety=k.VARIETY_REGULAR, exchange=k.EXCHANGE_NSE,
                                 product=k.PRODUCT_MIS, tag=TAG, **kw))

    def market(self, symbol, side, qty):
        try:
            oid = self._place(tradingsymbol=symbol, transaction_type=side, quantity=qty,
                              order_type=self.kite.ORDER_TYPE_MARKET)
        except Exception as e:
            return OrderResult("", "REJECTED", None, str(e))
        for _ in range(20):  # wait up to ~10s for the fill
            st = self.status(oid)
            if st.status in ("COMPLETE", "REJECTED", "CANCELLED"):
                return st
            time.sleep(0.5)
        return self.status(oid)

    def stop_loss(self, symbol, side, qty, trigger):
        # SL (trigger + protective limit) works on NSE cash; limit 0.5% beyond trigger.
        trig = tick(trigger)
        limit = tick(trig * (0.995 if side == "SELL" else 1.005))
        try:
            oid = self._place(tradingsymbol=symbol, transaction_type=side, quantity=qty,
                              order_type=self.kite.ORDER_TYPE_SL, trigger_price=trig, price=limit)
            return self.status(oid)
        except Exception as e:
            return OrderResult("", "REJECTED", None, str(e))

    def status(self, order_id):
        hist = self.kite.order_history(order_id)
        last = hist[-1] if hist else {}
        return OrderResult(order_id, last.get("status", "UNKNOWN"), last.get("average_price") or None,
                           last.get("status_message") or "")

    def cancel(self, order_id):
        try:
            self.kite.cancel_order(variety=self.kite.VARIETY_REGULAR, order_id=order_id)
        except Exception:
            pass  # already filled/cancelled

    def ltp(self, symbol):
        key = f"NSE:{symbol}"
        try:
            return float(self.kite.ltp([key])[key]["last_price"])
        except Exception:
            return None


class KiteFeed:
    """Real-time bars from Kite historical API (needs the paid Kite Connect plan)."""

    def __init__(self, broker: ZerodhaBroker):
        self.kite = broker.kite
        self._tokens = {i["tradingsymbol"]: i["instrument_token"] for i in self.kite.instruments("NSE")}

    def intraday(self, symbol, interval="5m", period="5d"):
        import datetime as dt

        import pandas as pd

        from ..data import _clean
        days = int(period.rstrip("d"))
        to = dt.datetime.now()
        rows = self.kite.historical_data(self._tokens[symbol], to - dt.timedelta(days=days + 3), to,
                                         interval.replace("m", "minute"))
        df = pd.DataFrame(rows).set_index("date") if rows else pd.DataFrame()
        return _clean(df)

    def daily(self, symbol, period="3mo"):
        import datetime as dt

        import pandas as pd

        from ..data import _clean
        to = dt.datetime.now()
        rows = self.kite.historical_data(self._tokens[symbol], to - dt.timedelta(days=100), to, "day")
        return _clean(pd.DataFrame(rows).set_index("date") if rows else pd.DataFrame())

    def ltp(self, symbol):
        key = f"NSE:{symbol}"
        return float(self.kite.ltp([key])[key]["last_price"])
