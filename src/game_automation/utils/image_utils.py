"""Image processing utilities."""

from __future__ import annotations

import io
from typing import Tuple

import numpy as np
from PIL import Image


def bytes_to_numpy(data: bytes) -> np.ndarray:
    """Convert raw PNG/JPEG bytes to an RGB numpy array."""
    image = Image.open(io.BytesIO(data)).convert("RGB")
    return np.array(image)


def numpy_to_pil(array: np.ndarray) -> Image.Image:
    """Convert an RGB numpy array to a PIL Image."""
    return Image.fromarray(array.astype("uint8"), "RGB")


def resize(array: np.ndarray, width: int, height: int) -> np.ndarray:
    """Resize *array* to (width, height)."""
    pil = numpy_to_pil(array).resize((width, height), Image.LANCZOS)
    return np.array(pil)


def crop(array: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Crop *array* to *bbox* = (x, y, w, h)."""
    x, y, w, h = bbox
    return array[y : y + h, x : x + w]


def save_image(array: np.ndarray, path: str) -> None:
    """Save *array* as an image file at *path*."""
    numpy_to_pil(array).save(path)
