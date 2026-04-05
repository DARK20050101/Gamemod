"""game_automation – Agent-based game automation and testing framework."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("game-automation")
except PackageNotFoundError:
    __version__ = "0.1.0"

from game_automation.agents.supervisor import SupervisorAgent
from game_automation.core.config import AppConfig

__all__ = [
    "__version__",
    "AppConfig",
    "SupervisorAgent",
]
