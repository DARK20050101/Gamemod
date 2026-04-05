"""Smoke tests – verify the package is importable and CLI works."""

from __future__ import annotations

import subprocess
import sys

import pytest


def test_import_package() -> None:
    """The package must be importable."""
    import game_automation  # noqa: F401

    assert hasattr(game_automation, "__version__")


def test_import_supervisor() -> None:
    from game_automation.agents.supervisor import SupervisorAgent  # noqa: F401


def test_import_app_config() -> None:
    from game_automation.core.config import AppConfig

    cfg = AppConfig()
    assert cfg.device.serial == "auto"
    assert cfg.agent.max_steps == 100


def test_import_models() -> None:
    from game_automation.models.action import Action, ActionType
    from game_automation.models.state import GameState
    from game_automation.models.result import AgentResult, ResultStatus

    action = Action(action_type=ActionType.WAIT, params={"seconds": 1})
    assert action.action_type == ActionType.WAIT

    state = GameState(step=0)
    assert state.step == 0

    result = AgentResult(status=ResultStatus.SUCCESS)
    assert result.status == ResultStatus.SUCCESS


def test_import_adapters() -> None:
    from game_automation.adapters.manager import AdapterManager

    manager = AdapterManager()
    assert manager.available() == []


def test_import_utils() -> None:
    from game_automation.utils.validation import validate_device_serial

    assert validate_device_serial("auto") is True
    assert validate_device_serial("emulator-5554") is True
    assert validate_device_serial("!bad") is False


def test_cli_help() -> None:
    """``python -m game_automation --help`` must exit 0 and print help text."""
    result = subprocess.run(
        [sys.executable, "-m", "game_automation", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "game-automation" in result.stdout.lower() or "usage" in result.stdout.lower()


def test_supervisor_agent_instantiation() -> None:
    """SupervisorAgent must instantiate without errors."""
    from game_automation.core.config import AppConfig
    from game_automation.agents.supervisor import SupervisorAgent

    cfg = AppConfig()
    agent = SupervisorAgent(config=cfg)
    assert agent.name == "SupervisorAgent"
