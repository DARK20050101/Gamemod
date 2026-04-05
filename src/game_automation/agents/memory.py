"""Memory agent – placeholder for state/experience storage."""

from __future__ import annotations

from collections import deque
from typing import Any, Deque, Dict, List, Optional

from game_automation.agents.base import BaseAgent
from game_automation.core.config import AppConfig
from game_automation.models.result import AgentResult, ResultStatus
from game_automation.models.state import GameState


class MemoryAgent(BaseAgent):
    """Stores and retrieves game states for context-aware decision making."""

    def __init__(self, config: Optional[AppConfig] = None, capacity: int = 100) -> None:
        super().__init__(config=config)
        self._buffer: Deque[GameState] = deque(maxlen=capacity)

    def remember(self, state: GameState) -> None:
        self._buffer.append(state)

    def recall(self, n: int = 1) -> List[GameState]:
        """Return the *n* most recent states."""
        items = list(self._buffer)
        return items[-n:]

    def clear(self) -> None:
        self._buffer.clear()

    def run(self) -> AgentResult:
        self.on_start()
        result = self._make_result(ResultStatus.SUCCESS, message="Memory ready")
        self.on_stop(result)
        return result
