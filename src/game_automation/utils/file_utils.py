"""File I/O utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


def ensure_dir(path: str) -> Path:
    """Create *path* as a directory (and parents) if it doesn't exist."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_yaml(path: str) -> Dict[str, Any]:
    """Load a YAML file and return its contents as a dict."""
    p = Path(path)
    if not p.exists():
        return {}
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return dict(data)


def save_yaml(data: Dict[str, Any], path: str) -> None:
    """Serialize *data* to a YAML file at *path*."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")


def read_text(path: str, encoding: str = "utf-8") -> str:
    return Path(path).read_text(encoding=encoding)


def write_text(path: str, content: str, encoding: str = "utf-8") -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)
