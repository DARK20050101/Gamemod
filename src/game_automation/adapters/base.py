"""Base game adapter interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseGameAdapter(ABC):
    """Abstract adapter that bridges the automation framework with a specific game."""

    #: Human-readable name for this adapter.
    name: str = "base"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config: Dict[str, Any] = config or {}

    @abstractmethod
    def is_running(self) -> bool:
        """Return True if the target game/app is currently in the foreground."""
        ...

    @abstractmethod
    def launch(self) -> bool:
        """Launch or bring the target game to the foreground. Returns True on success."""
        ...

    @abstractmethod
    def stop(self) -> bool:
        """Stop/close the target game. Returns True on success."""
        ...

    def get_package_name(self) -> str:
        """Return the Android package name (for ADB-based adapters)."""
        return self.config.get("package_name", "")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
