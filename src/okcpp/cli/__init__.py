"""CLI commands for ok-cpp."""

from pathlib import Path

# 获取 ok-cpp 安装根目录
# 模板现在在 okcpp 包内部：src/okcpp/templates 或 lib/okcpp/templates
_PKG_DIR = Path(__file__).parent.parent
ROOT_DIR = _PKG_DIR
TEMPLATES_DIR = _PKG_DIR / "templates"

# VERSION 文件在项目根目录（相对于包目录的上级）
# 开发环境: src/ 是包的父目录，VERSION 在项目根目录
# 安装环境: VERSION 与包目录在同一级
_VERSION_CANDIDATES = [
    _PKG_DIR.parent.parent / "VERSION",  # 开发环境: src/../VERSION
    _PKG_DIR.parent / "VERSION",         # 安装环境: lib/../VERSION
    Path("/usr/local/lib/okcpp") / "VERSION",  # 默认安装位置
]
VERSION_FILE = next((p for p in _VERSION_CANDIDATES if p.exists()), _VERSION_CANDIDATES[0])


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
  mkp (m)                Create a new CMake C++ project
  run (r)                Build & run a CMake project
  build-template (bt)    Create a custom template from existing project
  delete-template (dt)   Delete a custom template
  doctor (d)             Check development environment
  config (c)             config file
  help (h)               Show this help message

Options:
  -h, --help             Show help for a command
  -v, --version          Show version information

Examples:
  ok-cpp mkp demo/hello           (or: ok-cpp m demo/hello)
  ok-cpp run                      (or: ok-cpp r)
  ok-cpp run demo/hello           (or: ok-cpp r demo/hello)
  ok-cpp build-template ./my-proj -n my-template
  ok-cpp delete-template my-template
  ok-cpp doctor                   (or: ok-cpp d)""")


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
        "bt": "build-template",
        "dt": "delete-template",
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
    elif resolved == "build-template":
        from okcpp.cli import build_template
        return build_template.main(sys.argv[2:])
    elif resolved == "delete-template":
        from okcpp.cli import delete_template
        return delete_template.main(sys.argv[2:])
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
