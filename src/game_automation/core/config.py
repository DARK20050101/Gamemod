"""Application configuration management."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field


class DeviceConfig(BaseModel):
    serial: str = "auto"
    width: int = 1080
    height: int = 1920


class AgentConfig(BaseModel):
    max_steps: int = 100
    step_interval: float = 1.0
    screenshot_interval: float = 0.5


class LogConfig(BaseModel):
    level: str = "INFO"
    file: Optional[str] = None
    rotation: str = "10 MB"


class AppConfig(BaseModel):
    device: DeviceConfig = Field(default_factory=DeviceConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    log: LogConfig = Field(default_factory=LogConfig)
    adapters: dict[str, Any] = Field(default_factory=dict)
    extra: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str) -> AppConfig:
        """Load configuration from a YAML file."""
        config_path = Path(path)
        if not config_path.exists():
            return cls()
        data = yaml.safe_load(config_path.read_text()) or {}
        return cls(**data)

    def to_yaml(self, path: str) -> None:
        """Serialize configuration to a YAML file."""
        config_path = Path(path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        data = self.model_dump() if hasattr(self, "model_dump") else self.dict()
        config_path.write_text(yaml.safe_dump(data, allow_unicode=True))
