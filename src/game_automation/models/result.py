"""Agent result data model."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ResultStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    PARTIAL = "partial"


class AgentResult(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    status: ResultStatus
    steps_taken: int = 0
    message: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)
