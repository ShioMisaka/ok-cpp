"""Path handling utilities."""

from pathlib import Path


def abs_path(path: str | Path) -> Path:
    """将路径转换为绝对路径。

    类似于 bash 脚本中的 abs_path 函数：
    - 如果路径存在目录，返回其绝对路径
    - 如果路径是文件，返回文件的绝对路径
    - 如果路径不存在，返回基于当前目录的绝对路径

    Args:
        path: 输入路径（可以是相对或绝对路径）

    Returns:
        绝对路径的 Path 对象
    """
    p = Path(path)
    if not p:
        return Path()

    try:
        # 如果是目录且存在，直接返回绝对路径
        if p.is_dir():
            return p.resolve()

        # 如果是文件或路径不存在，返回其绝对路径
        # 对于不存在的路径，resolve() 仍然会返回规范化的绝对路径
        return p.expanduser().resolve()
    except Exception:
        # 如果 resolve 失败，尝试展开 ~ 并返回
        return p.expanduser()


def require_cmd(*commands: str) -> None:
    """检查指定的命令是否存在于 PATH 中。

    如果任何命令不存在，抛出异常。

    Args:
        *commands: 要检查的命令列表

    Raises:
        RuntimeError: 如果任何命令未找到
    """
    import shutil

    from okcpp.utils.log import die

    for cmd in commands:
        if shutil.which(cmd) is None:
            die(f"需要命令 '{cmd}'，但未找到。请先安装后重试。")


def get_cpu_count() -> int:
    """获取 CPU 核心数，用于并行编译。

    Returns:
        CPU 核心数，如果无法获取则返回 1
    """
    try:
        import os

        return os.cpu_count() or 1
    except Exception:
        return 1
