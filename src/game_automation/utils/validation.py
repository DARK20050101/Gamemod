"""Input validation helpers."""

from __future__ import annotations

import re


def validate_device_serial(serial: str) -> bool:
    """Return True if *serial* looks like a valid ADB device serial."""
    if serial in ("auto", ""):
        return True
    # Match patterns like: emulator-5554, 192.168.x.x:port, or alphanumeric serials
    pattern = r"^(emulator-\d+|(\d{1,3}\.){3}\d{1,3}:\d+|[A-Za-z0-9_:.-]{4,})$"
    return bool(re.match(pattern, serial))


def validate_positive_int(value: int, name: str = "value") -> int:
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer, got {value!r}")
    return value


def validate_float_range(value: float, lo: float, hi: float, name: str = "value") -> float:
    if not (lo <= value <= hi):
        raise ValueError(f"{name} must be in [{lo}, {hi}], got {value!r}")
    return value
