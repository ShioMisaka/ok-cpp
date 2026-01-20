"""build-template command - create custom template from existing project."""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from okcpp.cli import TEMPLATES_DIR
from okcpp.core.template import create_project
from okcpp.utils.log import die, info, print_blue, print_green_b, print_purple_b, print_yellow_b


def _get_okcpp_command() -> str:
    """获取 ok-cpp 命令的完整路径。

    Returns:
        ok-cpp 命令的绝对路径
    """
    # 尝试在 PATH 中查找 ok-cpp
    okcpp_path = shutil.which("ok-cpp")
    if okcpp_path:
        return okcpp_path

    # 如果 PATH 中找不到，使用开发环境中的 bin/ok-cpp
    script_dir = Path(__file__).parent.parent.parent.parent / "bin"
    okcpp_dev = script_dir / "ok-cpp"
    if okcpp_dev.exists():
        return str(okcpp_dev)

    # 最后尝试使用当前 Python 解释器直接运行
    return f"{sys.executable} -m okcpp.cli"


def print_usage() -> None:
    """打印使用说明。"""
    print("""Usage:
  ok-cpp build-template <source_path> -n <template_name> [options]

Arguments:
  source_path      Path to the existing project directory

Options:
  -n, --name <name>       Name for the new template (required)
  --skip-validate         Skip template validation (mkp + run test)
  -h, --help              Show this help message

Examples:
  ok-cpp build-template ./my-project -n my-template
  ok-cpp build-template ~/projects/cool-app -n cool-template --skip-validate""")


def validate_template_structure(source_dir: Path) -> bool:
    """验证模板目录结构是否有效。

    Args:
        source_dir: 源项目目录

    Returns:
        如果结构有效返回 True
    """
    cmake_file = source_dir / "CMakeLists.txt"

    if not cmake_file.exists():
        return False

    # 检查是否有 project() 声明
    try:
        content = cmake_file.read_text(encoding="utf-8")
        if not re.search(r"^\s*project\s*\(", content, re.MULTILINE | re.IGNORECASE):
            return False
    except Exception:
        return False

    return True


def validate_template_works(template_name: str, templates_dir: Path) -> bool:
    """验证模板是否可以正常工作（mkp + run 测试）。

    Args:
        template_name: 模板名称
        templates_dir: 模板目录

    Returns:
        如果模板可以正常工作返回 True
    """
    print_purple_b("[2/3] 验证模板可用性...")

    okcpp_cmd = _get_okcpp_command()

    with tempfile.TemporaryDirectory() as tmpdir:
        test_project = Path(tmpdir) / "test_project"

        # 使用 mkp 创建测试项目
        print_blue(f"  → 创建测试项目: {test_project}")
        try:
            create_project(
                target_path=str(test_project),
                template_name=template_name,
                project_name="test_project",
                templates_dir=templates_dir,
            )
        except Exception as e:
            print_yellow_b(f"  × 创建测试项目失败: {e}")
            return False

        # 尝试编译运行
        print_blue("  → 编译测试项目...")

        # 解析命令字符串
        if " -m " in okcpp_cmd:
            # Python module 方式: python3 -m okcpp.cli run path
            cmd_parts = okcpp_cmd.split()
            cmd = cmd_parts + ["run", str(test_project)]
        else:
            # 直接命令: /path/to/ok-cpp run path
            cmd = [okcpp_cmd, "run", str(test_project)]

        result = subprocess.run(
            cmd,
            cwd=test_project,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            print_yellow_b(f"  × 编译运行失败:")
            print(result.stderr)
            return False

        print_green_b("  ✓ 模板验证通过")
        return True


def main(args: list[str]) -> int:
    """build-template 命令主函数。

    Args:
        args: 命令行参数列表

    Returns:
        退出码
    """
    source_path = None
    template_name = None
    skip_validate = False

    # 解析参数
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-n", "--name"):
            if i + 1 < len(args):
                template_name = args[i + 1]
                i += 2
            else:
                die("选项 -n/--name 需要参数")
        elif arg == "--skip-validate":
            skip_validate = True
            i += 1
        elif arg in ("-h", "--help"):
            print_usage()
            return 0
        else:
            if source_path is None:
                source_path = arg
            else:
                die(f"未知参数或重复的源路径: {arg}")
            i += 1

    # 检查必需参数
    if not source_path:
        die("用法: ok-cpp build-template <source_path> -n <template_name>")
    if not template_name:
        die("选项 -n/--name 是必需的")

    source_dir = Path(source_path)
    if not source_dir.is_absolute():
        source_dir = Path.cwd() / source_dir

    # 检查源目录是否存在
    if not source_dir.exists():
        die(f"源目录不存在: {source_dir}")
    if not source_dir.is_dir():
        die(f"源路径不是目录: {source_dir}")

    print_purple_b("[1/3] 验证源项目结构...")

    # 验证模板结构
    if not validate_template_structure(source_dir):
        die(f"源项目不是有效的 CMake 项目（缺少 CMakeLists.txt 或 project() 声明）")

    print_green_b(f"  ✓ 源项目结构有效")

    # 检查目标模板是否已存在
    target_dir = TEMPLATES_DIR / template_name
    if target_dir.exists():
        die(f"模板已存在: {template_name} (路径: {target_dir})")

    # 复制模板
    print_purple_b("[2/3] 复制模板...")
    print_blue(f"  → 源: {source_dir}")
    print_blue(f"  → 目标: {target_dir}")

    try:
        shutil.copytree(source_dir, target_dir)
    except Exception as e:
        die(f"复制模板失败: {e}")

    print_green_b(f"  ✓ 模板已复制到: {target_dir}")

    # 验证模板
    if not skip_validate:
        if not validate_template_works(template_name, TEMPLATES_DIR):
            # 验证失败，删除已复制的模板
            print_yellow_b("  × 模板验证失败，正在删除...")
            shutil.rmtree(target_dir)
            die("模板验证失败，已取消创建")
    else:
        print_yellow_b("  → 跳过模板验证")

    # 成功
    print()
    print_green_b("模板创建成功!")
    print_yellow_b(f"Template name: {template_name}")
    print_blue(f"Template path: {target_dir}")
    info(f"现在可以使用 'ok-cpp mkp <path> -t {template_name}' 来创建项目")

    return 0
