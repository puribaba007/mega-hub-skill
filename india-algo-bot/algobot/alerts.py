"""Console + optional Telegram alerts. Token/chat id come only from env vars."""
from __future__ import annotations

import logging
import os

import requests

log = logging.getLogger("algobot")


class Alerts:
    def __init__(self, telegram: bool = False):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat = os.getenv("TELEGRAM_CHAT_ID")
        self.telegram = telegram and bool(self.token and self.chat)

    def send(self, msg: str) -> None:
        log.info(msg)
        if not self.telegram:
            return
        try:
            requests.post(f"https://api.telegram.org/bot{self.token}/sendMessage",
                          json={"chat_id": self.chat, "text": msg}, timeout=8)
        except Exception as e:  # alerts must never stop trading logic
            log.warning("telegram failed: %s", e)
