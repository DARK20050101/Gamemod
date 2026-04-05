"""Perception agent – captures and analyses the current screen."""

from __future__ import annotations

from game_automation.agents.base import BaseAgent
from game_automation.core.config import AppConfig
from game_automation.core.detector import Detector
from game_automation.core.device import Device
from game_automation.models.result import AgentResult, ResultStatus
from game_automation.models.state import GameState
from game_automation.utils.image_utils import bytes_to_numpy


class PerceptionAgent(BaseAgent):
    """Captures a screenshot and populates a GameState with detected elements."""

    def __init__(self, config: AppConfig | None = None, device: Device | None = None) -> None:
        super().__init__(config=config)
        self.device = device or Device(serial=self.config.device.serial)
        self.detector = Detector(threshold=0.8)

    def perceive(self) -> GameState:
        """Capture screen and return a populated GameState."""
        raw = self.device.screenshot()
        frame = bytes_to_numpy(raw)
        state = GameState(
            detected_elements={},
            metadata={"frame_shape": list(frame.shape)},
        )
        self.logger.debug(f"Perception: frame shape {frame.shape}")
        return state

    def run(self) -> AgentResult:
        self.on_start()
        self.perceive()
        result = self._make_result(ResultStatus.SUCCESS, steps=1, message="Perception complete")
        self.on_stop(result)
        return result
