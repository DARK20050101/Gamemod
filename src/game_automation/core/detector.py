"""Screen/image detector – template matching and object detection helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from game_automation.core.logger import get_logger

logger = get_logger(__name__)


class DetectionResult:
    """Holds a single detection hit."""

    def __init__(self, label: str, confidence: float, bbox: tuple[int, int, int, int]) -> None:
        self.label = label
        self.confidence = confidence
        # (x, y, width, height)
        self.bbox = bbox

    def center(self) -> tuple[int, int]:
        x, y, w, h = self.bbox
        return (x + w // 2, y + h // 2)

    def __repr__(self) -> str:
        return f"DetectionResult(label={self.label!r}, confidence={self.confidence:.2f}, bbox={self.bbox})"


class Detector:
    """Performs template matching and basic object detection on screenshots."""

    def __init__(self, threshold: float = 0.8) -> None:
        self.threshold = threshold

    def match_template(
        self,
        screenshot: np.ndarray,
        template_path: str,
    ) -> DetectionResult | None:
        """Return the best template match above the threshold, or None."""
        try:
            import cv2
        except ImportError:
            logger.warning("opencv-python not available; skipping template match")
            return None

        template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)
        if template is None:
            logger.error(f"Template not found: {template_path}")
            return None

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val < self.threshold:
            return None

        h, w = template.shape[:2]
        bbox = (max_loc[0], max_loc[1], w, h)
        label = Path(template_path).stem
        return DetectionResult(label=label, confidence=float(max_val), bbox=bbox)

    def find_all(
        self,
        screenshot: np.ndarray,
        template_path: str,
    ) -> list[DetectionResult]:
        """Return all matches above the threshold."""
        try:
            import cv2
        except ImportError:
            return []

        template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)
        if template is None:
            return []

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        h, w = template.shape[:2]
        label = Path(template_path).stem
        locations = np.where(result >= self.threshold)
        hits: list[DetectionResult] = []
        for pt in zip(*locations[::-1]):
            conf = float(result[pt[1], pt[0]])
            hits.append(DetectionResult(label=label, confidence=conf, bbox=(pt[0], pt[1], w, h)))
        return hits
