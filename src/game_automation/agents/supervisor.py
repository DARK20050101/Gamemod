"""Supervisor agent – orchestrates perception → decision → execution loop."""

from __future__ import annotations

from game_automation.agents.base import BaseAgent
from game_automation.agents.decision import DecisionAgent
from game_automation.agents.execution import ExecutionAgent
from game_automation.agents.perception import PerceptionAgent
from game_automation.core.config import AppConfig
from game_automation.core.device import Device
from game_automation.models.result import AgentResult, ResultStatus


class SupervisorAgent(BaseAgent):
    """Top-level orchestrator for the agent pipeline."""

    def __init__(self, config: AppConfig | None = None) -> None:
        super().__init__(config=config)
        device = Device(serial=self.config.device.serial)
        self.perception = PerceptionAgent(config=self.config, device=device)
        self.decision = DecisionAgent(config=self.config)
        self.execution = ExecutionAgent(config=self.config, device=device)

    def run(self) -> AgentResult:
        """Run the perception–decision–execution loop for *max_steps* steps."""
        self.on_start()
        max_steps = self.config.agent.max_steps
        steps = 0

        for step in range(max_steps):
            self.logger.info(f"Step {step + 1}/{max_steps}")
            # 1. Perceive
            try:
                state = self.perception.perceive()
            except Exception as exc:  # noqa: BLE001
                self.logger.warning(f"Perception error (step {step}): {exc}")
                break

            # 2. Decide
            action = self.decision.decide(state)
            if action is None:
                self.logger.info("No action – stopping loop.")
                break

            # 3. Execute
            success = self.execution.execute(action)
            steps += 1
            if not success:
                result = self._make_result(ResultStatus.FAILURE, steps=steps, message="Execution failed")
                self.on_stop(result)
                return result

        result = self._make_result(ResultStatus.SUCCESS, steps=steps, message="Loop completed")
        self.on_stop(result)
        return result
