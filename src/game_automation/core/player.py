"""Action player – replays recorded action sequences on a device."""

from __future__ import annotations

import time
from pathlib import Path

import yaml

from game_automation.core.logger import get_logger
from game_automation.models.action import Action, ActionType

logger = get_logger(__name__)


class Player:
    """Replays a YAML action sequence on a connected device."""

    def __init__(self, device_serial: str) -> None:
        self.device_serial = device_serial

    def play(self, file_path: str) -> None:
        """Load and execute actions from *file_path*."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Recording file not found: {path}")

        raw = yaml.safe_load(path.read_text()) or []
        actions: list[Action] = [Action(**item) for item in raw]
        logger.info(f"Playing {len(actions)} actions from {path}")

        for action in actions:
            self._execute(action)

    def _execute(self, action: Action) -> None:
        """Execute a single action on the device."""
        from game_automation.core.device import Device

        device = Device(serial=self.device_serial)

        if action.action_type == ActionType.TAP:
            x = int(action.params.get("x", 0))
            y = int(action.params.get("y", 0))
            logger.debug(f"TAP ({x}, {y})")
            device.tap(x, y)
        elif action.action_type == ActionType.SWIPE:
            device.swipe(
                int(action.params.get("x1", 0)),
                int(action.params.get("y1", 0)),
                int(action.params.get("x2", 0)),
                int(action.params.get("y2", 0)),
                int(action.params.get("duration_ms", 300)),
            )
        elif action.action_type == ActionType.WAIT:
            secs = float(action.params.get("seconds", 1.0))
            logger.debug(f"WAIT {secs}s")
            time.sleep(secs)
        else:
            logger.warning(f"Unknown action type: {action.action_type}")
