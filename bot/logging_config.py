"""Centralized logging configuration for the trading bot.

Provides setup_logging() to configure global logging to a file
with a consistent format and INFO level.
"""
import logging


def setup_logging() -> None:
    """Configure root logger to write INFO-level logs to bot.log.

    Idempotent: calling multiple times has no adverse effect.
    """
    logger = logging.getLogger()
    if logger.handlers:
        # Already configured — do nothing
        return

    logger.setLevel(logging.INFO)

    fmt = "%(asctime)s - %(levelname)s - %(message)s"
    handler = logging.FileHandler("bot.log")
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(fmt))

    logger.addHandler(handler)
