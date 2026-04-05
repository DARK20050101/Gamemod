"""Device abstraction layer (ADB-backed)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DeviceInfo:
    serial: str
    width: int = 1080
    height: int = 1920
    brand: str = "unknown"
    model: str = "unknown"


class Device:
    """Represents a connected device (physical or emulator)."""

    def __init__(self, serial: str = "auto") -> None:
        self.serial = serial
        self._info: Optional[DeviceInfo] = None

    def connect(self) -> bool:
        """Establish a connection to the device. Returns True on success."""
        from game_automation.utils.adb_utils import get_device_info

        try:
            self._info = get_device_info(self.serial)
            return True
        except Exception:  # noqa: BLE001
            return False

    def disconnect(self) -> None:
        """Release device connection."""
        self._info = None

    @property
    def info(self) -> Optional[DeviceInfo]:
        return self._info

    def screenshot(self) -> "bytes":
        """Capture a screenshot and return raw PNG bytes."""
        from game_automation.utils.adb_utils import take_screenshot

        return take_screenshot(self.serial)

    def tap(self, x: int, y: int) -> None:
        """Send a tap event to the device."""
        from game_automation.utils.adb_utils import adb_tap

        adb_tap(self.serial, x, y)

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
        """Send a swipe event to the device."""
        from game_automation.utils.adb_utils import adb_swipe

        adb_swipe(self.serial, x1, y1, x2, y2, duration_ms)

    def __repr__(self) -> str:
        return f"Device(serial={self.serial!r})"
