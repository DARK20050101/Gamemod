# game-automation

一个基于 **Agent 架构** 的游戏自动化测试与脚本框架（Python 3.9+，Poetry）。

本项目用于自动化功能测试、回归测试以及个人学习用途，适用于需要模拟设备交互的自动化脚本场景。

---

## 特性

- **感知 → 决策 → 执行** 三层 Agent 流水线架构
- 基于 ADB 的设备交互（点击、滑动、截图）
- OpenCV 模板匹配检测
- Pydantic 数据模型，配置驱动（YAML）
- 可扩展的适配器系统（`BaseGameAdapter` + `AdapterManager`）
- Typer CLI：`record` / `play` / `run`
- Loguru 日志，Rich 终端输出
- CI（ruff + mypy + pytest + coverage）

---

## 快速开始

### 环境要求

- Python 3.9+
- [Poetry](https://python-poetry.org/)
- ADB（Android Debug Bridge，用于设备操作）

### 安装

```bash
git clone https://github.com/DARK20050101/Gamemod.git
cd Gamemod
poetry install
```

### 使用示例

#### 查看帮助

```bash
poetry run game-automation --help
```

#### 录制操作

```bash
poetry run game-automation record --device emulator-5554 --output my_session.yaml
```

#### 回放录制

```bash
poetry run game-automation play my_session.yaml --device emulator-5554
```

#### 运行自动化

```bash
poetry run game-automation run --config configs/default.yaml --device emulator-5554
```

#### Python API

```python
from game_automation.core.config import AppConfig, AgentConfig, DeviceConfig
from game_automation.agents.supervisor import SupervisorAgent

config = AppConfig(
    device=DeviceConfig(serial="emulator-5554"),
    agent=AgentConfig(max_steps=10, step_interval=1.0),
)
agent = SupervisorAgent(config=config)
result = agent.run()
print(result.status, result.steps_taken)
```

---

## 项目结构

```
src/game_automation/
├── __init__.py          # 包入口，导出 __version__
├── __main__.py          # python -m game_automation
├── cli.py               # Typer CLI
├── core/                # 核心模块
│   ├── config.py
│   ├── device.py
│   ├── detector.py
│   ├── logger.py
│   ├── player.py
│   └── recorder.py
├── agents/              # Agent 流水线
│   ├── base.py
│   ├── perception.py
│   ├── decision.py
│   ├── execution.py
│   ├── supervisor.py
│   └── memory.py
├── adapters/            # 游戏适配器
│   ├── base.py
│   └── manager.py
├── models/              # Pydantic 数据模型
│   ├── action.py
│   ├── config.py
│   ├── result.py
│   └── state.py
└── utils/               # 工具函数
    ├── adb_utils.py
    ├── file_utils.py
    ├── image_utils.py
    └── validation.py
configs/
└── default.yaml
tests/unit/
└── test_smoke.py
examples/
└── basic_usage.py
```

---

## 开发

```bash
# 安装开发依赖
poetry install

# 运行测试
poetry run pytest

# 代码检查
poetry run ruff check src/ tests/
poetry run mypy src/game_automation

# 安装 pre-commit hooks
poetry run pre-commit install
```

---

## 许可证

MIT © 2024 DARK20050101
