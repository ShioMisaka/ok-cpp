"""CMake build logic for ok-cpp."""

import os
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from okcpp.utils.log import (
    colored,
    err,
    handle_error,
    info,
    print_blue,
    print_blue_b,
    print_purple_b,
    print_yellow_b,
)


@dataclass
class BuildConfig:
    """构建配置。"""

    compiler: str = "gun"  # "gun" or "clang"
    build_type: str = "Release"  # "Debug" or "Release"
    project_name: Optional[str] = None
    project_dir: Path = Path(".")
    build_dir: Path = Path("build")

    # 编译器环境变量
    cc: Optional[str] = None
    cxx: Optional[str] = None
    # CMake 生成器
    generator: str = "Unix Makefiles"


def get_cmake_project_name(cmake_dir: Path) -> Optional[str]:
    """从 CMakeLists.txt 中解析 project 名。

    支持的格式：
    - project(foo)
    - project(foo LANGUAGES CXX)
    - project(foo VERSION 1.0)

    Args:
        cmake_dir: 包含 CMakeLists.txt 的目录

    Returns:
        项目名称，如果解析失败则返回 None
    """
    cmake_file = cmake_dir / "CMakeLists.txt"
    if not cmake_file.exists():
        return None

    try:
        content = cmake_file.read_text(encoding="utf-8")
        # 匹配 project(...) 语法，忽略大小写
        match = re.search(
            r"^\s*project\s*\(\s*([A-Za-z0-9_-]+)",
            content,
            re.MULTILINE | re.IGNORECASE,
        )
        if match:
            return match.group(1)
    except Exception:
        pass

    return None


def find_project_dir(arg: Optional[str], current_dir: Path = None) -> Optional[Path]:
    """查找项目目录。

    查找顺序：
    1. 如果 arg 是包含 CMakeLists.txt 的目录，使用该目录
    2. 如果 arg 的父目录包含 CMakeLists.txt，使用父目录
    3. 按 project_name 在当前目录下搜索（最大深度 4）

    Args:
        arg: 命令行参数（路径或项目名）
        current_dir: 当前工作目录，默认为当前目录

    Returns:
        项目目录的绝对路径，如果未找到则返回 None
    """
    if current_dir is None:
        current_dir = Path.cwd()

    if arg is None:
        # 使用当前目录
        if (current_dir / "CMakeLists.txt").exists():
            return current_dir
        return None

    arg_path = Path(arg)

    # 检查是否是包含 CMakeLists.txt 的目录
    if arg_path.is_dir() and (arg_path / "CMakeLists.txt").exists():
        return arg_path.resolve()

    # 检查父目录
    if arg_path.exists():
        parent = arg_path.parent
        if (parent / "CMakeLists.txt").exists():
            return parent.resolve()

    # 按项目名搜索
    try:
        # 使用 find 搜索包含 CMakeLists.txt 且目录名匹配的目录
        result = subprocess.run(
            ["find", ".", "-maxdepth", "4", "-type", "f", "-name", "CMakeLists.txt"],
            capture_output=True,
            text=True,
            cwd=current_dir,
            timeout=10,
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                cmake_dir = Path(line).parent
                if cmake_dir.name == arg:
                    return cmake_dir.resolve()
    except Exception:
        pass

    return None


def setup_compiler_env(config: BuildConfig) -> BuildConfig:
    """设置编译器环境变量和 CMake 生成器。

    Args:
        config: 构建配置

    Returns:
        更新后的构建配置
    """
    if config.compiler == "gun":
        config.cc = "gcc"
        config.cxx = "g++"
        config.generator = "Unix Makefiles"
    elif config.compiler == "clang":
        config.cc = "clang"
        config.cxx = "clang++"
        config.generator = "Ninja"
    else:
        err(f"未知编译器: {config.compiler} (使用 gun / clang)")
        raise ValueError(f"Unknown compiler: {config.compiler}")

    return config


def check_build_cache_needs_clean(build_dir: Path, compiler: str, build_type: str) -> bool:
    """检查是否需要清理构建缓存。

    如果编译器或构建类型发生变化，需要清理构建目录。

    Args:
        build_dir: 构建目录
        compiler: 当前编译器
        build_type: 当前构建类型

    Returns:
        如果需要清理返回 True
    """
    mark_file = build_dir / "compiler.txt"
    build_type_file = build_dir / "build_type.txt"

    if not build_dir.exists():
        return False

    needs_clean = False

    if mark_file.exists():
        prev_compiler = mark_file.read_text().strip()
        if prev_compiler != compiler:
            needs_clean = True

    if build_type_file.exists():
        prev_build_type = build_type_file.read_text().strip()
        if prev_build_type != build_type:
            needs_clean = True

    return needs_clean


def clean_build_dir(build_dir: Path) -> None:
    """清理构建目录。

    Args:
        build_dir: 构建目录
    """
    import shutil

    if build_dir.exists():
        print_yellow_b("配置变更，清理 build 目录")
        shutil.rmtree(build_dir)


def write_build_markers(build_dir: Path, compiler: str, build_type: str) -> None:
    """写入构建标记文件。

    Args:
        build_dir: 构建目录
        compiler: 编译器
        build_type: 构建类型
    """
    build_dir.mkdir(parents=True, exist_ok=True)
    (build_dir / "compiler.txt").write_text(compiler)
    (build_dir / "build_type.txt").write_text(build_type)


def run_cmake_configure(config: BuildConfig) -> bool:
    """运行 CMake 配置。

    Args:
        config: 构建配置

    Returns:
        如果成功返回 True
    """
    print_purple_b("[1/3] CMake Configure")

    env = os.environ.copy()
    if config.cc:
        env["CC"] = config.cc
    if config.cxx:
        env["CXX"] = config.cxx

    cmd = [
        "cmake",
        "-B", str(config.build_dir),
        "-G", config.generator,
        f"-DCMAKE_BUILD_TYPE={config.build_type}",
    ]

    start = time.time()
    try:
        subprocess.run(
            cmd,
            cwd=config.project_dir,
            env=env,
            check=True,
        )
        duration = time.time() - start
        print_blue(f"Configure finished in {duration:.2f}s.")
        return True
    except subprocess.CalledProcessError:
        return False


def run_cmake_build(config: BuildConfig) -> bool:
    """运行 CMake 构建。

    Args:
        config: 构建配置

    Returns:
        如果成功返回 True
    """
    print_purple_b("[2/3] Build")

    cmd = ["cmake", "--build", str(config.build_dir)]

    start = time.time()
    try:
        subprocess.run(
            cmd,
            cwd=config.project_dir,
            check=True,
        )
        duration = time.time() - start
        print_blue(f"Compilation finished in {duration:.2f}s.")
        return True
    except subprocess.CalledProcessError:
        return False


def get_executable_path(config: BuildConfig) -> Path:
    """获取可执行文件路径。

    对于库模板，会尝试查找 ${PROJECT_NAME}_test 作为回退选项。

    Args:
        config: 构建配置

    Returns:
        可执行文件的路径
    """
    if config.project_name:
        exe_path = config.build_dir / config.project_name
        # 如果主可执行文件不存在，尝试查找 _test 后缀的（用于库模板）
        if not exe_path.exists():
            test_path = config.build_dir / f"{config.project_name}_test"
            if test_path.exists():
                return test_path
        return exe_path
    # 如果没有项目名，使用目录名
    return config.build_dir / config.project_dir.name


def run_executable(exe_path: Path, build_type: str) -> int:
    """运行可执行文件或启动调试器。

    Args:
        exe_path: 可执行文件路径
        build_type: 构建类型

    Returns:
        退出码
    """
    if not exe_path.exists():
        err(f"未找到可执行文件: {exe_path}")
        return 1

    if build_type == "Debug":
        # 检查 gdb 是否存在
        import shutil

        if shutil.which("gdb") is None:
            err("Debug 模式需要 GDB，但未找到。请先安装。")
            return 1

        print_purple_b("[3/3] Debug (GDB)")
        print("=" * 70)
        result = subprocess.run(["gdb", str(exe_path)])
        print("=" * 70)
        return result.returncode
    else:
        print_purple_b("[3/3] Run Executable")
        print("=" * 70)
        result = subprocess.run([str(exe_path)])
        print("=" * 70)
        return result.returncode


def build_and_run(config: BuildConfig) -> int:
    """执行完整的构建和运行流程。

    Args:
        config: 构建配置

    Returns:
        退出码
    """
    # 1. 设置编译器环境
    config = setup_compiler_env(config)

    print_yellow_b(f"项目路径: {config.project_dir}")

    # 2. 解析项目名
    if config.project_name is None:
        config.project_name = get_cmake_project_name(config.project_dir)
        if config.project_name:
            info(f"Detected project name from CMake: {config.project_name}")
        else:
            config.project_name = config.project_dir.name
            info(f"未检测到 project(...)，回退为目录名: {config.project_name}")

    print_blue_b(f"Compiler: {config.cxx}")
    print_blue_b(f"Build type: {config.build_type}")

    # 3. 检查是否需要清理构建缓存
    if check_build_cache_needs_clean(config.build_dir, config.compiler, config.build_type):
        clean_build_dir(config.build_dir)

    # 4. 写入构建标记
    write_build_markers(config.build_dir, config.compiler, config.build_type)

    # 5. CMake 配置
    if not run_cmake_configure(config):
        handle_error("CMake 配置失败")
        return 1

    # 6. CMake 构建
    if not run_cmake_build(config):
        handle_error("编译失败")
        return 1

    # 7. 运行可执行文件
    exe_path = get_executable_path(config)
    return run_executable(exe_path, config.build_type)
