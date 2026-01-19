# Python 代码风格规则

适用于 ok-cpp 项目的 Python 代码编写规范。

## 路径操作

**优先使用 `pathlib.Path` 而非 `os.path`**

```python
# 推荐
from pathlib import Path
config_file = Path.home() / ".config" / "ok-cpp" / "config"

# 避免
import os
config_file = os.path.expanduser("~/.config/ok-cpp/config")
```

## 数据结构

**使用 `dataclass` 定义配置和状态数据**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class BuildConfig:
    compiler: str = "gun"
    build_type: str = "Release"
    project_name: Optional[str] = None
    project_dir: Path = Path(".")
```

## 类型注解

**所有公共函数应添加类型注解**

```python
def find_project_dir(arg: Optional[str], current_dir: Path = None) -> Optional[Path]:
    """查找项目目录。

    Args:
        arg: 命令行参数（路径或项目名）
        current_dir: 当前工作目录，默认为当前目录

    Returns:
        项目目录的绝对路径，如果未找到则返回 None
    """
```

## 日志输出

**使用 `okcpp.utils.log` 模块的彩色输出函数**

```python
from okcpp.utils.log import (
    info, warn, err, die,
    print_blue, print_green_b, print_yellow_b, print_purple_b
)

# 信息输出
info("正在编译...")
print_blue(f"Compiler: {config.cxx}")

# 成功/警告/错误
print_green_b("构建成功")
print_yellow_b("配置已更改")
err("编译失败")
die("未找到 CMakeLists.txt")

# 分节输出
print_purple_b("[1/3] CMake Configure")
```

## 模块组织

**代码应按职责放置在对应的目录中**

```
lib/okcpp/
├── cli/           # CLI 命令模块 (run.py, mkp.py, doctor.py, config.py)
│   └── __init__.py # 命令调度器
├── core/          # 核心业务逻辑 (builder.py, template.py, detector.py)
├── utils/         # 工具函数 (log.py, path.py, config.py)
└── templates/     # 项目模板
```

## 错误处理

**使用适当的错误处理方式**

```python
# 可恢复的错误：返回 False 或 None
def run_cmake_configure(config: BuildConfig) -> bool:
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# 致命错误：使用 die()
if not cmake_file.exists():
    die(f"未找到 CMakeLists.txt: {cmake_file}")

# 预期的异常：捕获并处理
try:
    content = file.read_text(encoding="utf-8")
except UnicodeDecodeError:
    warn("文件编码问题，使用备用编码")
    content = file.read_text(encoding="latin-1")
```

## 命令行参数解析

**当前使用手动参数解析，保持一致性**

```python
def main(args: list[str]) -> int:
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-t", "--template"):
            if i + 1 < len(args):
                template_name = args[i + 1]
                i += 2
            else:
                die("选项 -t/--template 需要参数")
        # ...
    return 0
```

## 文档字符串

**使用 Google 风格的文档字符串**

```python
def create_project(
    target_path: str,
    template_name: str,
    project_name: str,
    templates_dir: Path,
) -> Path:
    """从模板创建项目。

    Args:
        target_path: 目标路径（可以是相对或绝对路径）
        template_name: 模板名称
        project_name: 项目名称（用于 CMake project()）
        templates_dir: 模板根目录

    Returns:
        创建的项目目录的绝对路径
    """
```

## 导入顺序

```python
# 1. 标准库
import os
import re
from pathlib import Path
from typing import Optional

# 2. 第三方库
from rich.console import Console

# 3. 本地模块
from okcpp.utils.log import info
from okcpp.core.builder import BuildConfig
```
