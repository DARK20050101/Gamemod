"""ADB utility helpers."""

from __future__ import annotations

import subprocess
from typing import List

from game_automation.core.logger import get_logger

logger = get_logger(__name__)


def _run_adb(serial: str, *args: str, timeout: int = 10) -> bytes:
    """Run an ADB command for *serial* and return stdout bytes."""
    cmd: List[str] = ["adb"]
    if serial and serial != "auto":
        cmd += ["-s", serial]
    cmd += list(args)
    result = subprocess.run(cmd, capture_output=True, timeout=timeout)
    if result.returncode != 0:
        raise RuntimeError(f"ADB error: {result.stderr.decode(errors='replace').strip()}")
    return result.stdout


def get_device_info(serial: str) -> "game_automation.core.device.DeviceInfo":  # type: ignore[name-defined]
    """Query device properties and return a DeviceInfo instance."""
    from game_automation.core.device import DeviceInfo

    brand = _run_adb(serial, "shell", "getprop", "ro.product.brand").decode().strip()
    model = _run_adb(serial, "shell", "getprop", "ro.product.model").decode().strip()
    size_raw = _run_adb(serial, "shell", "wm", "size").decode().strip()
    # typical output: "Physical size: 1080x1920"
    width, height = 1080, 1920
    if "x" in size_raw:
        parts = size_raw.split()[-1].split("x")
        try:
            width, height = int(parts[0]), int(parts[1])
        except (ValueError, IndexError):
            pass
    return DeviceInfo(serial=serial, width=width, height=height, brand=brand, model=model)


def take_screenshot(serial: str) -> bytes:
    """Capture a screenshot from the device and return raw PNG bytes."""
    return _run_adb(serial, "exec-out", "screencap", "-p", timeout=30)


def adb_tap(serial: str, x: int, y: int) -> None:
    _run_adb(serial, "shell", "input", "tap", str(x), str(y))
    logger.debug(f"[{serial}] tap ({x}, {y})")


def adb_swipe(serial: str, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
    _run_adb(serial, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms))
    logger.debug(f"[{serial}] swipe ({x1},{y1})->({x2},{y2}) {duration_ms}ms")
