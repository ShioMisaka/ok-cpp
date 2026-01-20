"""Doctor command - check development environment."""

from okcpp.core.detector import (
    check_build_tools,
    check_compilers,
    check_debug_tools,
    check_qt,
    run_doctor,
)
from okcpp.utils.log import info, ok, print_section, warn


def main(args: list[str]) -> int:
    """Doctor 命令主函数。

    Args:
        args: 命令行参数列表

    Returns:
        退出码
    """
    info("ok-cpp doctor - environment check")

    # 编译器
    print_section("C++ Compilers")
    compilers = check_compilers()
    has_compiler = False
    for compiler in compilers:
        if compiler.installed:
            ok(str(compiler))
            has_compiler = True
        else:
            warn(str(compiler))

    if not has_compiler:
        warn("No C++ compiler found (install g++ or clang++)")

    # 构建工具
    print_section("Build Tools")
    build_tools = check_build_tools()
    for tool in build_tools.values():
        if tool.installed:
            ok(str(tool))
        else:
            if tool.command == "ninja":
                warn(f"{tool.name}: not found (optional, recommended)")
            else:
                warn(str(tool))

    # 调试工具
    print_section("Debug Tools")
    debug_tools = check_debug_tools()
    for tool in debug_tools.values():
        if tool.installed:
            ok(str(tool))
        else:
            warn(f"{tool.name}: not found (required for Debug mode)")

    # Qt
    print_section("Qt (Template Dependency)")
    qt = check_qt()
    if qt.installed:
        ok(str(qt))
    else:
        warn(str(qt))
        info("  Hint: install qtbase-dev / qt6-base-dev")

    # 总结
    print()
    info("Doctor check finished.")
    info("If something is missing, install it and re-run: ok-cpp doctor")

    return 0
