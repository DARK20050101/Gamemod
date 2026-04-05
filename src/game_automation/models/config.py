"""Model-related configuration (e.g. detector model paths)."""

from __future__ import annotations

from pydantic import BaseModel


class ModelConfig(BaseModel):
    detector_weights: str | None = None
    confidence_threshold: float = 0.8
    device: str = "cpu"
