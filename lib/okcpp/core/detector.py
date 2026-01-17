"""Environment detection for ok-cpp."""

import shutil
import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class ToolInfo:
    """工具信息。"""

    name: str
    command: str
    installed: bool = False
    version: Optional[str] = None

    def __str__(self) -> str:
        """返回工具信息的字符串表示。"""
        if self.installed:
            version_str = self.version or ""
            return f"✔ {self.name}: {version_str}"
        return f"✘ {self.name}: not found"


def check_command(name: str, command: str) -> ToolInfo:
    """检查命令是否存在并获取版本。

    Args:
        name: 工具显示名称
        command: 命令名称

    Returns:
        ToolInfo 对象
    """
    path = shutil.which(command)
    if path is None:
        return ToolInfo(name=name, command=command, installed=False)

    version = _get_version(command)
    return ToolInfo(name=name, command=command, installed=True, version=version)


def _get_version(command: str) -> Optional[str]:
    """获取命令的版本信息。

    Args:
        command: 命令名称

    Returns:
        版本字符串，如果无法获取则返回 None
    """
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            # 取第一行作为版本
            return result.stdout.splitlines()[0].strip()
    except Exception:
        pass

    # 如果 --version 不工作，尝试其他方式
    try:
        result = subprocess.run(
            [command, "-v"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.splitlines()[0].strip()
    except Exception:
        pass

    return None


def check_compilers() -> list[ToolInfo]:
    """检查 C++ 编译器。

    Returns:
        编译器信息列表
    """
    compilers = [
        ToolInfo(name="GCC (g++)", command="g++"),
        ToolInfo(name="Clang (clang++)", command="clang++"),
    ]

    results = []
    for compiler in compilers:
        path = shutil.which(compiler.command)
        if path is not None:
            version = _get_version(compiler.command)
            results.append(
                ToolInfo(name=compiler.name, command=compiler.command, installed=True, version=version)
            )
        else:
            results.append(
                ToolInfo(name=compiler.name, command=compiler.command, installed=False)
            )

    return results


def check_build_tools() -> dict[str, ToolInfo]:
    """检查构建工具。

    Returns:
        工具名称到 ToolInfo 的映射
    """
    return {
        "cmake": check_command("CMake", "cmake"),
        "ninja": check_command("Ninja", "ninja"),
    }


def check_debug_tools() -> dict[str, ToolInfo]:
    """检查调试工具。

    Returns:
        工具名称到 ToolInfo 的映射
    """
    return {
        "gdb": check_command("GDB", "gdb"),
    }


def check_qt() -> ToolInfo:
    """检查 Qt 是否安装。

    Returns:
        Qt 工具信息
    """
    # 检查 qmake
    qmake_path = shutil.which("qmake")
    if qmake_path is not None:
        version = _get_qt_version("qmake")
        return ToolInfo(name="Qt (qmake)", command="qmake", installed=True, version=version)

    # 检查 qtpaths
    qtpaths_path = shutil.which("qtpaths")
    if qtpaths_path is not None:
        return ToolInfo(name="Qt (qtpaths)", command="qtpaths", installed=True, version="detected")

    return ToolInfo(name="Qt", command="", installed=False)


def _get_qt_version(command: str) -> Optional[str]:
    """获取 Qt 版本。

    Args:
        command: 命令名称 (qmake)

    Returns:
        版本字符串
    """
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            # qmake 输出格式通常是：
            # QMake version 3.1
            # Using Qt version 5.15.2 in /usr/lib
            for line in result.stdout.splitlines():
                if "Qt version" in line:
                    return line.strip()
            return result.stdout.splitlines()[0].strip()
    except Exception:
        pass

    return None


def run_doctor() -> dict:
    """运行完整的环境检测。

    Returns:
        包含所有检测结果的字典
    """
    return {
        "compilers": check_compilers(),
        "build_tools": check_build_tools(),
        "debug_tools": check_debug_tools(),
        "qt": check_qt(),
    }
