"""Centralised logging configuration using loguru."""

from __future__ import annotations

import sys
from typing import Any

from loguru import logger as _logger


def get_logger(name: str = "game_automation") -> Any:
    """Return a configured loguru logger bound with *name*."""
    return _logger.bind(name=name)


def configure_logging(level: str = "INFO", log_file: str | None = None, rotation: str = "10 MB") -> None:
    """Configure global logging sinks."""
    _logger.remove()
    _logger.add(sys.stderr, level=level, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[name]}</cyan> – {message}")
    if log_file:
        _logger.add(log_file, level=level, rotation=rotation, encoding="utf-8")
