"""Action recorder – captures user interactions and saves them to YAML."""

from __future__ import annotations

import time
from pathlib import Path
from typing import List

import yaml

from game_automation.core.logger import get_logger
from game_automation.models.action import Action

logger = get_logger(__name__)


class Recorder:
    """Records device interactions into a YAML action sequence."""

    def __init__(self, device_serial: str, output_path: str = "recording.yaml") -> None:
        self.device_serial = device_serial
        self.output_path = Path(output_path)
        self._actions: List[Action] = []

    def start(self) -> None:
        """Start an interactive recording session (stub – extend with real ADB input monitor)."""
        logger.info(f"Recorder started for device {self.device_serial}")
        logger.info("Recording stub – no real events captured in this MVP.")
        self._save()

    def add_action(self, action: Action) -> None:
        self._actions.append(action)

    def _save(self) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        data = [a.model_dump() if hasattr(a, "model_dump") else a.dict() for a in self._actions]
        self.output_path.write_text(yaml.safe_dump(data, allow_unicode=True))
        logger.info(f"Recording saved to {self.output_path} ({len(self._actions)} actions)")
