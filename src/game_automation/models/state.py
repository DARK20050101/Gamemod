"""Game state data model."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GameState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    step: int = 0
    screen_hash: str | None = None
    detected_elements: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
