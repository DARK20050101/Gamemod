"""Base agent abstract class."""

from __future__ import annotations

from abc import ABC, abstractmethod

from game_automation.core.config import AppConfig
from game_automation.core.logger import get_logger
from game_automation.models.result import AgentResult, ResultStatus


class BaseAgent(ABC):
    """Abstract base for all agents in the pipeline."""

    def __init__(self, config: AppConfig | None = None, name: str | None = None) -> None:
        self.config = config or AppConfig()
        self.name = name or self.__class__.__name__
        self.logger = get_logger(self.name)

    @abstractmethod
    def run(self) -> AgentResult:
        """Execute the agent's main loop."""
        ...

    def on_start(self) -> None:
        """Hook called before *run*."""
        self.logger.info(f"Agent [{self.name}] starting.")

    def on_stop(self, result: AgentResult) -> None:
        """Hook called after *run*."""
        self.logger.info(f"Agent [{self.name}] stopped with status={result.status}.")

    def _make_result(
        self,
        status: ResultStatus = ResultStatus.SUCCESS,
        steps: int = 0,
        message: str | None = None,
    ) -> AgentResult:
        return AgentResult(status=status, steps_taken=steps, message=message)
