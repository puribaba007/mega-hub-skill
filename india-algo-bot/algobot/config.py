"""Load config.yaml into a simple attribute-access object."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import yaml

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


def _ns(obj: Any) -> Any:
    if isinstance(obj, dict):
        return SimpleNamespace(**{k: _ns(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [_ns(v) for v in obj]
    return obj


def load_config(path: str | Path | None = None) -> SimpleNamespace:
    path = Path(path) if path else DEFAULT_PATH
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    cfg = _ns(raw)
    validate(cfg)
    return cfg


def validate(cfg: SimpleNamespace) -> None:
    if cfg.mode not in ("paper", "live"):
        raise ValueError("mode must be 'paper' or 'live'")
    if cfg.mode == "live" and cfg.broker == "paper":
        raise ValueError("live mode needs a real broker (e.g. broker: zerodha)")
    r = cfg.risk
    if not 0 < r.risk_per_trade_pct <= 2:
        raise ValueError("risk_per_trade_pct must be in (0, 2] — protect your capital")
    if not 0 < r.max_daily_loss_pct <= 5:
        raise ValueError("max_daily_loss_pct must be in (0, 5]")
    if r.leverage < 1 or r.leverage > 5:
        raise ValueError("leverage must be between 1 and 5")
    if cfg.strategy.name not in ("orb", "vwap_pullback"):
        raise ValueError("strategy.name must be 'orb' or 'vwap_pullback'")
