"""delete-template command - delete a custom template."""

import shutil
from pathlib import Path

from okcpp.cli import TEMPLATES_DIR
from okcpp.core.template import list_templates
from okcpp.utils.log import die, info, print_blue, print_green_b, print_red_b, print_yellow_b


def print_usage() -> None:
    """打印使用说明。"""
    print("""Usage:
  ok-cpp delete-template <template_name> [options]

Arguments:
  template_name     Name of the template to delete

Options:
  -f, --force       Skip confirmation prompt
  -h, --help        Show this help message

Examples:
  ok-cpp delete-template my-template
  ok-cpp delete-template my-template --force
  ok-cpp dt my-template              # 使用别名""")


def confirm_delete(template_name: str) -> bool:
    """确认是否删除模板。

    Args:
        template_name: 模板名称

    Returns:
        用户确认返回 True，否则返回 False
    """
    print_yellow_b(f"即将删除模板: {template_name}")
    print(f"模板路径: {TEMPLATES_DIR / template_name}")
    print()
    response = input("确认删除? (y/N): ").strip().lower()
    return response in ("y", "yes")


def list_available_templates() -> None:
    """列出可用的模板。"""
    templates = list_templates(TEMPLATES_DIR)
    if not templates:
        print_yellow_b("没有可用的模板")
        return

    print_blue("可用的模板:")
    for template in templates:
        print(f"  - {template}")


def main(args: list[str]) -> int:
    """delete-template 命令主函数。

    Args:
        args: 命令行参数列表

    Returns:
        退出码
    """
    template_name = None
    force = False

    # 解析参数
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-f", "--force"):
            force = True
            i += 1
        elif arg in ("-h", "--help"):
            print_usage()
            return 0
        else:
            if template_name is None:
                template_name = arg
            else:
                die(f"未知参数或重复的模板名: {arg}")
            i += 1

    # 检查必需参数
    if not template_name:
        die("用法: ok-cpp delete-template <template_name>")

    # 检查模板是否存在
    template_dir = TEMPLATES_DIR / template_name
    if not template_dir.exists():
        print_red_b(f"模板不存在: {template_name}")
        print()
        print_blue("可用的模板:")
        list_available_templates()
        return 1

    # 确认删除
    if not force:
        if not confirm_delete(template_name):
            print_yellow_b("已取消删除")
            return 0

    # 删除模板
    print_blue(f"删除模板: {template_name}")
    try:
        shutil.rmtree(template_dir)
    except Exception as e:
        die(f"删除模板失败: {e}")

    print_green_b(f"模板已删除: {template_name}")
    info(f"使用 'ok-cpp mkp --list' 查看剩余模板")

    return 0
