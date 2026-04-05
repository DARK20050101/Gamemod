"""Decision agent – selects the next action given a GameState."""

from __future__ import annotations

from game_automation.agents.base import BaseAgent
from game_automation.core.config import AppConfig
from game_automation.models.action import Action, ActionType
from game_automation.models.result import AgentResult, ResultStatus
from game_automation.models.state import GameState


class DecisionAgent(BaseAgent):
    """Rule-based decision engine that maps game states to actions."""

    def __init__(self, config: AppConfig | None = None) -> None:
        super().__init__(config=config)

    def decide(self, state: GameState) -> Action | None:
        """Return the next Action given *state*, or None if no action is needed."""
        # Stub: always wait – override in subclasses with real logic.
        return Action(action_type=ActionType.WAIT, params={"seconds": self.config.agent.step_interval})

    def run(self) -> AgentResult:
        self.on_start()
        result = self._make_result(ResultStatus.SUCCESS, steps=1, message="Decision complete")
        self.on_stop(result)
        return result
