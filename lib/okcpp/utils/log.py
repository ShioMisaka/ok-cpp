"""Logging utilities with colored output using rich."""

import sys
from typing import Optional

from rich.console import Console
from rich.text import Text

# 全局 console 实例
console = Console()

# ANSI 颜色代码（用于不使用 rich 的场景）
class AnsiColor:
    """ANSI 颜色代码。"""

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"

    RED_B = "\033[1;31m"
    GREEN_B = "\033[1;32m"
    YELLOW_B = "\033[1;33m"
    BLUE_B = "\033[1;34m"
    PURPLE_B = "\033[1;35m"

    RESET = "\033[0m"


def _format_message(prefix: str, prefix_style: str, message: str) -> Text:
    """格式化带前缀的消息。

    Args:
        prefix: 前缀文本 (如 [OK], [INFO])
        prefix_style: 前缀样式
        message: 消息内容

    Returns:
        格式化后的 Text 对象
    """
    text = Text()
    text.append(prefix, style=prefix_style)
    text.append(" ")
    text.append(message)
    return text


def ok(message: str) -> None:
    """输出成功消息（绿色 [OK]）。

    Args:
        message: 消息内容
    """
    text = _format_message("[OK]", "bold green", message)
    console.print(text)


def info(message: str) -> None:
    """输出信息消息（绿色 [INFO]）。

    Args:
        message: 消息内容
    """
    text = _format_message("[INFO]", "bold green", message)
    console.print(text)


def warn(message: str) -> None:
    """输出警告消息（黄色 [WARN]）。

    Args:
        message: 消息内容
    """
    text = _format_message("[WARN]", "bold yellow", message)
    console.print(text)


def err(message: str) -> None:
    """输出错误消息（红色 [ERR]）。

    Args:
        message: 消息内容
    """
    text = _format_message("[ERR]", "bold red", message)
    console.print(text)


def die(message: str, exit_code: int = 1) -> None:
    """输出错误消息并退出程序。

    Args:
        message: 错误消息
        exit_code: 退出码，默认为 1
    """
    err(message)
    sys.exit(exit_code)


def handle_error(message: str) -> None:
    """处理构建错误，显示错误并等待用户按回车退出。

    Args:
        message: 错误消息
    """
    console.print(f"[Error] {message}", style="red")
    input("Press Enter to exit...")
    sys.exit(1)


# 颜色常量，用于直接在消息中使用
class Color:
    """终端颜色常量。"""

    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    PURPLE = "purple"
    RESET = "reset"


def colored(message: str, color: str) -> str:
    """返回带颜色的消息字符串（用于 console.print）。

    Args:
        message: 消息内容
        color: 颜色名称

    Returns:
        带颜色标记的字符串
    """
    return f"[{color}]{message}[/{color}]"


# 更多颜色输出函数
def print_blue(message: str) -> None:
    """输出蓝色消息。

    Args:
        message: 消息内容
    """
    console.print(message, style="blue")


def print_blue_b(message: str) -> None:
    """输出加粗蓝色消息。

    Args:
        message: 消息内容
    """
    console.print(message, style="bold blue")


def print_yellow(message: str) -> None:
    """输出黄色消息。

    Args:
        message: 消息内容
    """
    console.print(message, style="yellow")


def print_yellow_b(message: str) -> None:
    """输出加粗黄色消息。

    Args:
        message: 消息内容
    """
    console.print(message, style="bold yellow")


def print_purple(message: str) -> None:
    """输出紫色消息。

    Args:
        message: 消息内容
    """
    console.print(message, style="purple")


def print_purple_b(message: str) -> None:
    """输出加粗紫色消息。

    Args:
        message: 消息内容
    """
    console.print(message, style="bold purple")


def print_green(message: str) -> None:
    """输出绿色消息。

    Args:
        message: 消息内容
    """
    console.print(message, style="green")


def print_green_b(message: str) -> None:
    """输出加粗绿色消息。

    Args:
        message: 消息内容
    """
    console.print(message, style="bold green")


def print_red(message: str) -> None:
    """输出红色消息。

    Args:
        message: 消息内容
    """
    console.print(message, style="red")


def print_red_b(message: str) -> None:
    """输出加粗红色消息。

    Args:
        message: 消息内容
    """
    console.print(message, style="bold red")


def print_section(title: str) -> None:
    """打印分节标题（蓝色）。

    Args:
        title: 标题文本
    """
    print()
    print_purple_b(f"= {title} =")
