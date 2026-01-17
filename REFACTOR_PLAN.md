# ok-cpp Python 重构计划

## 目标

将 ok-cpp 从 shell 脚本完全重构为 Python 实现，保持功能完全一致，同时提升代码可维护性和可扩展性。

## 技术选型

| 项目 | 选择 |
|------|------|
| Python 版本 | 3.8+ (使用 dataclass, typing, pathlib) |
| 项目结构 | 包结构模块化 |
| 依赖管理 | 允许轻量依赖 (rich, typer) |
| 安装方式 | 保持 install.sh 兼容 |
| CLI 框架 | **typer** (已确认) |
| 开发方式 | **分阶段实施** (已确认) |

## 新项目结构

```
ok-cpp/
├── bin/
│   └── ok-cpp              # Python 入口脚本 (shebang)
├── lib/
│   └── okcpp/              # Python 包根目录
│       ├── __init__.py
│       ├── __main__.py     # 模块执行入口
│       ├── cli/            # CLI 命令模块
│       │   ├── __init__.py
│       │   ├── run.py      # run 命令
│       │   ├── mkp.py      # mkp 命令
│       │   ├── doctor.py   # doctor 命令
│       │   └── config.py   # config 命令
│       ├── core/           # 核心功能
│       │   ├── __init__.py
│       │   ├── builder.py  # CMake 构建逻辑
│       │   ├── template.py # 模板处理
│       │   └── detector.py # 环境检测
│       ├── utils/          # 工具函数
│       │   ├── __init__.py
│       │   ├── log.py      # 日志/颜色输出
│       │   ├── path.py     # 路径处理
│       │   └── config.py   # 配置文件管理
│       └── templates/      # 保持原有模板目录
│           ├── default/
│           └── qt/
├── install.sh              # 更新：安装 Python 包
├── uninstall.sh            # 更新：卸载 Python 包
├── pyproject.toml          # 新增：Python 项目配置
├── requirements.txt        # 新增：依赖声明
├── VERSION                 # 保持
├── README.md
└── CLAUDE.md
```

## 模块映射关系

| Shell 模块 | Python 模块 | 说明 |
|-----------|-------------|------|
| `bin/ok-cpp` | `bin/ok-cpp` + `cli/__init__.py` | 命令分发、别名解析 |
| `common.sh` | `utils/` | 全部拆分到各 utils 模块 |
| `cmd_run.sh` | `cli/run.py` + `core/builder.py` | 构建逻辑独立到 core |
| `cmd_mkp.sh` | `cli/mkp.py` + `core/template.py` | 模板处理独立到 core |
| `cmd_doctor.sh` | `cli/doctor.py` + `core/detector.py` | 检测逻辑独立到 core |
| `cmd_config.sh` | `cli/config.py` + `utils/config.py` | 配置管理在 utils |
| `install.sh` | 更新为安装 Python 包 | 复制 lib/ 到安装目录 |
| `uninstall.sh` | 保持不变 | 路径调整 |

## 依赖库

```
# requirements.txt
rich>=13.0.0           # 终端颜色、进度条
typer>=0.9.0           # CLI 框架 (基于 click，类型注解友好)
```

## 实现步骤

### Phase 1: 基础框架搭建

1. **创建 Python 包结构**
   - 创建 `lib/okcpp/` 目录和 `__init__.py`
   - 设置 `pyproject.toml`
   - 创建 `requirements.txt`

2. **实现 utils 模块**
   - `utils/log.py`: 颜色日志输出（使用 rich）
   - `utils/path.py`: 绝对路径处理
   - `utils/config.py`: 配置文件读写

3. **实现新的入口脚本**
   - `bin/ok-cpp` 作为 Python shebang 脚本
   - 实现命令分发和别名解析
   - 实现 `--version` 和 `--help`

### Phase 2: 核心功能实现

4. **实现 core/detector.py**
   - 命令存在性检查
   - 版本获取
   - Qt 检测

5. **实现 core/builder.py**
   - CMake 项目名解析
   - 编译器配置 (gcc/clang)
   - 构建类型管理 (Debug/Release)
   - 构建缓存清理逻辑
   - CMake 配置和构建执行

6. **实现 core/template.py**
   - 模板列表获取
   - 模板复制
   - CMakeLists.txt 项目名替换

### Phase 3: CLI 命令实现

7. **实现 cli/doctor.py**
   - 复用 core/detector
   - 输出格式对齐原版

8. **实现 cli/config.py**
   - show/set/reset 子命令
   - 参数验证

9. **实现 cli/mkp.py**
   - 参数解析 (-t, -n, --list)
   - 调用 core/template

10. **实现 cli/run.py**
    - 参数解析 (-d, -c, -p)
    - 项目目录查找逻辑
    - 调用 core/builder
    - 执行/GDB 启动

### Phase 4: 安装脚本更新

11. **更新 install.sh**
    - 检查 Python 版本
    - 安装依赖 (pip install -r requirements.txt)
    - 复制 lib/ 到目标目录
    - 更新 shebang 路径

12. **更新 uninstall.sh**
    - 路径调整

### Phase 5: 测试与完善

13. **功能测试**
    - 逐一测试每个命令
    - 对比输出格式

14. **文档更新**
    - 更新 CLAUDE.md
    - 添加 Python 开发说明

## 关键实现细节

### 1. 日志输出 (utils/log.py)

使用 `rich.console` 和 `rich.text` 实现颜色输出：

```python
from rich.console import Console
from rich.text import Text

console = Console()

def ok(msg: str) -> None:
    text = Text()
    text.append("[OK] ", style="bold green")
    text.append(msg)
    console.print(text)

def info(msg: str) -> None:
    text = Text()
    text.append("[INFO] ", style="bold green")
    text.append(msg)
    console.print(text)

def warn(msg: str) -> None:
    # ...

def err(msg: str) -> None:
    # ...

def die(msg: str) -> None:
    err(msg)
    sys.exit(1)
```

### 2. CMake 项目名解析 (core/builder.py)

使用正则表达式解析：

```python
import re
from pathlib import Path

def get_cmake_project_name(cmake_dir: Path) -> str | None:
    cmake_file = cmake_dir / "CMakeLists.txt"
    if not cmake_file.exists():
        return None

    content = cmake_file.read_text()
    # 匹配: project(foo), project(foo LANGUAGES CXX), project(foo VERSION 1.0)
    match = re.search(r'^\s*project\s*\(\s*([A-Za-z0-9_-]+)', content, re.MULTILINE | re.IGNORECASE)
    return match.group(1) if match else None
```

### 3. 配置文件管理 (utils/config.py)

使用 `pathlib` 和简单的 key-value 解析：

```python
from pathlib import Path
from dataclasses import dataclass, field
import os

@dataclass
class Config:
    compiler: str = "gun"
    template_name: str = "default"

    _config_dir: Path = field(init=False)
    _config_file: Path = field(init=False)

    def __post_init__(self):
        self._config_dir = Path(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))) / "ok-cpp"
        self._config_file = self._config_dir / "config"

    def load(self) -> None:
        if self._config_file.exists():
            # 解析简单的 KEY=value 格式
            for line in self._config_file.read_text().splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    key, value = line.split("=", 1)
                    if key == "COMPILER":
                        self.compiler = value
                    elif key == "TEMPLATE_NAME":
                        self.template_name = value

    def save(self) -> None:
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._config_file.write_text(
            f"# ok-cpp user config (auto-generated)\n"
            f"\n"
            f"COMPILER={self.compiler}\n"
            f"TEMPLATE_NAME={self.template_name}\n"
        )
```

### 4. 命令分发 (cli/__init__.py 或 bin/ok-cpp)

```python
# bin/ok-cpp
#!/usr/bin/env python3
import sys
from pathlib import Path

# 添加 lib/ 到 Python 路径
lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(lib_dir))

from okcpp.cli import main

if __name__ == "__main__":
    sys.exit(main())
```

```python
# okcpp/cli/__init__.py
import sys

COMMAND_ALIASES = {
    "m": "mkp",
    "r": "run",
    "d": "doctor",
    "c": "config",
    "h": "help",
}

def main():
    if len(sys.argv) < 2:
        print_help()
        return 0

    cmd = sys.argv[1]
    resolved = COMMAND_ALIASES.get(cmd, cmd)

    if cmd in ("-v", "--version"):
        print_version()
        return 0
    if cmd in ("-h", "--help"):
        print_help()
        return 0

    # 导入并执行对应命令模块
    if resolved == "mkp":
        from okcpp.cli import mkp
        return mkp.main(sys.argv[2:])
    elif resolved == "run":
        from okcpp.cli import run
        return run.main(sys.argv[2:])
    # ...
```

## 与原版本保持一致的细节

1. **输出格式**: 保持 `[OK]`, `[INFO]`, `[WARN]`, `[ERR]` 前缀和颜色
2. **错误消息**: 保持中文错误消息
3. **配置文件格式**: 保持 `KEY=value` 格式，确保向后兼容
4. **模板系统**: 保持完全一致的模板目录结构和 CMakeLists.txt
5. **命令别名**: 保持 m/r/d/c/h 快捷方式

## 开发工作流

```bash
# 开发时使用 PYTHONPATH 直接运行
export PYTHONPATH=/path/to/ok-cpp/lib:$PYTHONPATH
python3 -m okcpp run

# 或者直接运行 bin/ok-cpp
./bin/ok-cpp run

# 测试安装
sudo ./install.sh
ok-cpp run
```

## 待确认问题

- [ ] 是否需要添加单元测试？
- [ ] 是否需要支持 Windows (通过 WSL 或 MinGW)？
- [ ] 是否需要添加新的功能（如更多模板）？
