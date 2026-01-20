"""Config command - manage user configuration."""

import os
from pathlib import Path

from okcpp.utils.config import Config, get_config, reset_config
from okcpp.utils.log import die, err, info, print_blue, print_green_b, print_yellow_b


def print_usage() -> None:
    """打印使用说明。"""
    print("""Usage:
  ok-cpp config show
  ok-cpp config set <key> <value>
  ok-cpp config reset

Config keys:
  compiler        default compiler for 'ok-cpp run'   (clang | gun)
  template        default template for 'ok-cpp mkp'

Examples:
  ok-cpp config show
  ok-cpp config set compiler clang
  ok-cpp config set template qt
  ok-cpp config reset""")


def cmd_show() -> int:
    """显示当前配置。

    Returns:
        退出码
    """
    config = get_config()
    config_base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    config_file = Path(config_base) / "ok-cpp" / "config"

    print_yellow_b(f"Config file: {config_file}")
    print()
    print_blue(f"COMPILER={config.compiler}")
    print_blue(f"TEMPLATE_NAME={config.template_name}")

    return 0


def cmd_set(key: str, value: str) -> int:
    """设置配置项。

    Args:
        key: 配置键
        value: 配置值

    Returns:
        退出码
    """
    config = get_config()

    if key == "compiler":
        if not config.validate_compiler(value):
            die(f"Invalid compiler: {value} (clang | gun)")
        config.compiler = value
    elif key == "template":
        if not config.validate_template(value):
            die(f"Template not found: {value}")
        config.template_name = value
    else:
        die(f"Unknown config key: {key}")

    config.save()
    print_green_b(f"Config updated: {key}={value}")

    return 0


def cmd_reset() -> int:
    """重置配置。

    Returns:
        退出码
    """
    config_base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    config_file = Path(config_base) / "ok-cpp" / "config"

    if config_file.exists():
        config_file.unlink()
        info("Config reset (using defaults)")
    else:
        info("No config file found")

    reset_config()
    return 0


def main(args: list[str]) -> int:
    """Config 命令主函数。

    Args:
        args: 命令行参数列表

    Returns:
        退出码
    """
    if not args:
        return cmd_show()

    cmd = args[0]

    if cmd in ("-h", "--help", "help"):
        print_usage()
        return 0

    if cmd == "show":
        return cmd_show()

    if cmd == "set":
        if len(args) < 3:
            err("Usage: ok-cpp config set <key> <value>")
            return 1
        return cmd_set(args[1], args[2])

    if cmd == "reset":
        return cmd_reset()

    err(f"Unknown config command: {cmd}")
    print_usage()
    return 1
