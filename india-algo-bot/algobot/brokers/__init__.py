from .base import Broker, OrderResult
from .paper import PaperBroker


def make_broker(cfg, feed):
    if cfg.broker == "paper":
        return PaperBroker(feed, cfg.costs.slippage_bps)
    if cfg.broker == "zerodha":
        from .zerodha import ZerodhaBroker
        return ZerodhaBroker()
    raise ValueError(f"unknown broker {cfg.broker!r}")


__all__ = ["Broker", "OrderResult", "PaperBroker", "make_broker"]
