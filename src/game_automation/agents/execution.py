"""Execution agent – sends actions to the device."""

from __future__ import annotations

from game_automation.agents.base import BaseAgent
from game_automation.core.config import AppConfig
from game_automation.core.device import Device
from game_automation.models.action import Action, ActionType
from game_automation.models.result import AgentResult, ResultStatus


class ExecutionAgent(BaseAgent):
    """Translates Action objects into device commands."""

    def __init__(self, config: AppConfig | None = None, device: Device | None = None) -> None:
        super().__init__(config=config)
        self.device = device or Device(serial=self.config.device.serial)

    def execute(self, action: Action) -> bool:
        """Execute *action* on the device. Returns True on success."""
        import time

        try:
            if action.action_type == ActionType.TAP:
                self.device.tap(int(action.params["x"]), int(action.params["y"]))
            elif action.action_type == ActionType.SWIPE:
                self.device.swipe(
                    int(action.params["x1"]),
                    int(action.params["y1"]),
                    int(action.params["x2"]),
                    int(action.params["y2"]),
                    int(action.params.get("duration_ms", 300)),
                )
            elif action.action_type == ActionType.WAIT:
                time.sleep(float(action.params.get("seconds", 1.0)))
            else:
                self.logger.warning(f"Unhandled action type: {action.action_type}")
            return True
        except Exception as exc:  # noqa: BLE001
            self.logger.error(f"Execution failed: {exc}")
            return False

    def run(self) -> AgentResult:
        self.on_start()
        result = self._make_result(ResultStatus.SUCCESS, steps=1, message="Execution ready")
        self.on_stop(result)
        return result
