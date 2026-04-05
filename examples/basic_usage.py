"""Basic usage example – initialise SupervisorAgent and run one step."""

from __future__ import annotations

from game_automation.core.config import AppConfig, AgentConfig, DeviceConfig
from game_automation.agents.supervisor import SupervisorAgent


def main() -> None:
    # Build a minimal config (no real device needed for a dry-run)
    config = AppConfig(
        device=DeviceConfig(serial="emulator-5554"),
        agent=AgentConfig(max_steps=1, step_interval=0.0),
    )

    agent = SupervisorAgent(config=config)
    print(f"Starting {agent.name} …")

    # NOTE: This will attempt to connect to the device via ADB.
    # In a real scenario, make sure the emulator/device is running first.
    result = agent.run()
    print(f"Result: status={result.status}, steps={result.steps_taken}, msg={result.message}")


if __name__ == "__main__":
    main()
