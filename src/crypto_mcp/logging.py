import logging
import sys

from pythonjsonlogger.json import JsonFormatter


def setup_logging(level: int = logging.INFO) -> None:
    """Configure structured JSON logging for the MCP server."""
    logger = logging.getLogger()
    logger.setLevel(level)

    # We must use stderr so we don't interfere with stdio JSON-RPC
    log_handler = logging.StreamHandler(sys.stderr)
    formatter = JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={
            "levelname": "level",
            "asctime": "timestamp",
        },
    )
    log_handler.setFormatter(formatter)

    # Remove existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(log_handler)
