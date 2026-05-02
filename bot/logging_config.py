"""Logging configuration."""
import logging


def setup_logging() -> None:
    """Initialize root logger to write INFO-level logs to bot.log."""
    logger = logging.getLogger()
    if logger.handlers:
        return

    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("bot.log")
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
