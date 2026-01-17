"""Mkp command - create project from template."""

from okcpp.cli import TEMPLATES_DIR
from okcpp.core.template import create_project, list_templates
from okcpp.utils.config import get_config
from okcpp.utils.log import die, info, print_green_b, print_yellow_b


def print_usage() -> None:
    """打印使用说明。"""
    print("""Usage:
  ok-cpp mkp <path> [options]

Arguments:
  path              Target directory for the project

Options:
  -t, --template <name>   Template to use (default or qt)
  -n, --name <name>       Project name for CMake project()
  -l, --list              List available templates

Examples:
  ok-cpp mkp demos/hello
  ok-cpp mkp demos/qt_app -t qt
  ok-cpp mkp demos/app -n my_app
  ok-cpp mkp --list""")


def cmd_list_templates() -> int:
    """列出可用模板。

    Returns:
        退出码
    """
    print_yellow_b("可用模板：")
    templates = list_templates(TEMPLATES_DIR)
    for template in templates:
        print_green_b(f"  - {template}")
    return 0


def main(args: list[str]) -> int:
    """Mkp 命令主函数。

    Args:
        args: 命令行参数列表

    Returns:
        退出码
    """
    # 加载用户配置获取默认模板
    config = get_config()
    template_name = config.template_name or "default"
    project_name = ""
    list_only = False
    positional = []

    # 解析参数
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-t", "--template"):
            if i + 1 < len(args):
                template_name = args[i + 1]
                i += 2
            else:
                die("选项 -t/--template 需要参数")
        elif arg in ("-n", "--name"):
            if i + 1 < len(args):
                project_name = args[i + 1]
                i += 2
            else:
                die("选项 -n/--name 需要参数")
        elif arg in ("-l", "--list"):
            list_only = True
            i += 1
        elif arg in ("-h", "--help"):
            print_usage()
            return 0
        else:
            positional.append(arg)
            i += 1

    # 列出模板
    if list_only:
        return cmd_list_templates()

    # 检查目标路径
    if not positional:
        die("用法: ok-cpp mkp <path> [options]")

    target_path = positional[0]

    # 创建项目
    create_project(
        target_path=target_path,
        template_name=template_name,
        project_name=project_name,
        templates_dir=TEMPLATES_DIR,
    )

    return 0
