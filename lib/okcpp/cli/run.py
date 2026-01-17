"""Run command - build and run CMake project."""

from pathlib import Path

from okcpp.core.builder import BuildConfig, build_and_run, find_project_dir
from okcpp.utils.config import get_config
from okcpp.utils.log import die
from okcpp.utils.path import require_cmd


def main(args: list[str]) -> int:
    """Run 命令主函数。

    Args:
        args: 命令行参数列表

    Returns:
        退出码
    """
    # 检查 CMake 是否存在
    require_cmd("cmake")

    # 加载用户配置获取默认编译器
    config = get_config()

    # 默认值
    build_config = BuildConfig(
        compiler=config.compiler or "gun",
        build_type="Release",
        project_dir=Path.cwd(),
        build_dir=Path("build"),
    )

    # 解析参数
    positional = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-d", "--debug"):
            build_config.build_type = "Debug"
            i += 1
        elif arg in ("-c", "--compiler"):
            if i + 1 < len(args):
                build_config.compiler = args[i + 1]
                i += 2
            else:
                die("选项 -c/--compiler 需要参数")
        elif arg in ("-p", "--project"):
            if i + 1 < len(args):
                build_config.project_name = args[i + 1]
                i += 2
            else:
                die("选项 -p/--project 需要参数")
        elif arg in ("gun", "clang"):
            build_config.compiler = arg
            i += 1
        else:
            positional.append(arg)
            i += 1

    # 确定项目目录
    if positional:
        arg = positional[0]
        project_dir = find_project_dir(arg)
        if project_dir is None:
            die(f"未找到项目: {arg}")
        build_config.project_dir = project_dir
    else:
        # 使用当前目录
        if not (Path.cwd() / "CMakeLists.txt").exists():
            die("当前目录没有 CMakeLists.txt")
        build_config.project_dir = Path.cwd()

    # 设置相对构建目录
    build_config.build_dir = build_config.project_dir / "build"

    # 执行构建和运行
    return build_and_run(build_config)
