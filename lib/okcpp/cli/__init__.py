"""CLI commands for ok-cpp."""

from pathlib import Path

# 获取 ok-cpp 安装根目录
# 当作为包安装时，使用 __file__ 的父目录
# 当开发时，从 lib/okcpp 推导
_ROOT_DIR = Path(__file__).parent.parent.parent.parent
if (_ROOT_DIR / "lib" / "ok-cpp" / "templates").exists():
    # 开发环境: 使用 lib/ok-cpp
    ROOT_DIR = _ROOT_DIR / "lib" / "ok-cpp"
else:
    # 安装环境: 使用包目录
    ROOT_DIR = Path(__file__).parent.parent

TEMPLATES_DIR = ROOT_DIR / "templates"
VERSION_FILE = ROOT_DIR.parent.parent / "VERSION"


def get_version() -> str:
    """Get ok-cpp version from VERSION file."""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return "unknown"


def print_version() -> None:
    """Print version information."""
    print(f"ok-cpp version {get_version()}")


def print_help() -> None:
    """Print help message."""
    print("""ok-cpp - C++ learning playground (CMake based)

Usage:
  ok-cpp <command> [options]

Commands:
  mkp (m)           Create a new CMake C++ project
  run (r)           Build & run a CMake project
  doctor (d)        Check development environment
  config (c)        config file
  help (h)          Show this help message

Options:
  -h, --help        Show help for a command
  -v, --version     Show version information

Examples:
  ok-cpp mkp demo/hello  (or: ok-cpp m demo/hello)
  ok-cpp run             (or: ok-cpp r)
  ok-cpp run demo/hello  (or: ok-cpp r demo/hello)
  ok-cpp doctor          (or: ok-cpp d)""")


def main() -> int:
    """Main entry point for CLI."""
    import sys

    if len(sys.argv) < 2:
        print_help()
        return 0

    cmd = sys.argv[1]

    if cmd in ("-v", "--version"):
        print_version()
        return 0
    if cmd in ("-h", "--help"):
        print_help()
        return 0

    # 命令别名映射
    aliases = {
        "m": "mkp",
        "r": "run",
        "d": "doctor",
        "c": "config",
        "h": "help",
    }

    resolved = aliases.get(cmd, cmd)

    if resolved == "help":
        print_help()
        return 0

    # 导入并执行对应命令
    if resolved == "mkp":
        from okcpp.cli import mkp
        return mkp.main(sys.argv[2:])
    elif resolved == "run":
        from okcpp.cli import run
        return run.main(sys.argv[2:])
    elif resolved == "doctor":
        from okcpp.cli import doctor
        return doctor.main(sys.argv[2:])
    elif resolved == "config":
        from okcpp.cli import config
        return config.main(sys.argv[2:])
    else:
        print(f"Unknown command: {cmd}")
        print()
        print_help()
        return 1
