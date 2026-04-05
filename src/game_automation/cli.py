"""Typer-based CLI for game-automation."""

from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer(
    name="game-automation",
    help="Agent-based game automation and testing framework.",
    add_completion=False,
)
console = Console()


@app.command()
def record(
    device: str = typer.Option(..., "--device", "-d", help="ADB device serial ID."),
    output: str = typer.Option("recording.yaml", "--output", "-o", help="Output file path."),
) -> None:
    """Record user actions on a connected device."""
    console.print(f"[bold green]Recording[/] on device [cyan]{device}[/] → {output}")
    from game_automation.core.recorder import Recorder

    rec = Recorder(device_serial=device, output_path=output)
    rec.start()


@app.command()
def play(
    file: str = typer.Argument(..., help="Recording file to replay."),
    device: str = typer.Option(..., "--device", "-d", help="ADB device serial ID."),
) -> None:
    """Replay a previously recorded session."""
    console.print(f"[bold blue]Playing[/] {file} on device [cyan]{device}[/]")
    from game_automation.core.player import Player

    player = Player(device_serial=device)
    player.play(file)


@app.command()
def run(
    config: str = typer.Option("configs/default.yaml", "--config", "-c", help="Config file path."),
    device: str = typer.Option("auto", "--device", "-d", help="ADB device serial ID."),
) -> None:
    """Run the SupervisorAgent automation loop."""
    console.print(f"[bold magenta]Running[/] automation with config [yellow]{config}[/] on device [cyan]{device}[/]")
    from game_automation.agents.supervisor import SupervisorAgent
    from game_automation.core.config import AppConfig

    app_config = AppConfig.from_yaml(config)
    agent = SupervisorAgent(config=app_config)
    agent.run()


if __name__ == "__main__":
    app()
