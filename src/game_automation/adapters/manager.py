"""Adapter manager – registry and lifecycle management for game adapters."""

from __future__ import annotations

from typing import Dict, Optional, Type

from game_automation.adapters.base import BaseGameAdapter
from game_automation.core.logger import get_logger

logger = get_logger(__name__)


class AdapterManager:
    """Registry for :class:`BaseGameAdapter` implementations."""

    def __init__(self) -> None:
        self._registry: Dict[str, Type[BaseGameAdapter]] = {}
        self._active: Dict[str, BaseGameAdapter] = {}

    def register(self, adapter_cls: Type[BaseGameAdapter]) -> None:
        """Register an adapter class by its *name* attribute."""
        self._registry[adapter_cls.name] = adapter_cls
        logger.debug(f"Adapter registered: {adapter_cls.name}")

    def get(self, name: str, config: Optional[dict] = None) -> BaseGameAdapter:
        """Return an instantiated adapter by *name*, creating it if needed."""
        if name not in self._active:
            if name not in self._registry:
                raise KeyError(f"No adapter registered with name {name!r}. Available: {list(self._registry)}")
            self._active[name] = self._registry[name](config=config)
        return self._active[name]

    def available(self) -> list:
        return list(self._registry.keys())

    def shutdown_all(self) -> None:
        """Stop all active adapters."""
        for name, adapter in self._active.items():
            try:
                adapter.stop()
                logger.info(f"Adapter {name!r} stopped.")
            except Exception as exc:  # noqa: BLE001
                logger.warning(f"Error stopping adapter {name!r}: {exc}")
        self._active.clear()
