"""Action data model."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class ActionType(str, Enum):
    TAP = "tap"
    SWIPE = "swipe"
    WAIT = "wait"
    KEY = "key"
    TEXT = "text"
    SCREENSHOT = "screenshot"
    CUSTOM = "custom"


class Action(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    action_type: ActionType
    params: Dict[str, Any] = Field(default_factory=dict)
    description: Optional[str] = None
    timestamp: Optional[float] = None
