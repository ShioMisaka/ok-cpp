#!/usr/bin/env bash
# cmd_run.sh - ok-cpp run
set -euo pipefail

# ==========================================================
# 基础路径 & 公共函数
# ==========================================================
ROOT_DIR="${OK_CPP_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
COMMON="$ROOT_DIR/lib/ok-cpp/common.sh"

# shellcheck source=/dev/null
source "$COMMON"

require_cmd cmake

# ==========================================================
# 默认值
# ==========================================================
COMPILER="gun"
PROJECT_NAME=""
BUILD_DIR="build"
BUILD_TYPE="Release"

load_user_config
COMPILER="${COMPILER:-gun}"

# ==========================================================
# 参数解析
# ==========================================================
POSITIONAL=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        -d|--debug)
            BUILD_TYPE="Debug"
            shift
            ;;
        -c|--compiler)
            COMPILER="$2"
            shift 2
            ;;
        -p|--project)
            PROJECT_NAME="$2"
            shift 2
            ;;
        gun|clang)
            COMPILER="$1"
            shift
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

# ==========================================================
# 确定项目目录
# ==========================================================
PROJECT_DIR=""

if [[ ${#POSITIONAL[@]} -ge 1 ]]; then
    arg="${POSITIONAL[0]}"
    if [[ -d "$arg" && -f "$arg/CMakeLists.txt" ]]; then
        PROJECT_DIR="$(abs_path "$arg")"
    elif [[ -f "$arg/CMakeLists.txt" ]]; then
        PROJECT_DIR="$(abs_path "$(dirname "$arg")")"
    else
        # 按项目名查找
        found="$(find . -maxdepth 4 -type f -name CMakeLists.txt \
                -exec dirname {} \; 2>/dev/null \
                | grep "/$arg$" | head -n 1 || true)"
        [[ -n "$found" ]] || die "未找到项目: $arg"
        PROJECT_DIR="$(abs_path "$found")"
    fi
else
    [[ -f "./CMakeLists.txt" ]] || die "当前目录没有 CMakeLists.txt"
    PROJECT_DIR="$(pwd)"
fi

cd "$PROJECT_DIR"

info "项目路径: ${YELLOW}$PROJECT_DIR${RESET}"

# ==========================================================
# 解析 project name
# ==========================================================
if [[ -z "$PROJECT_NAME" ]]; then
    if PROJECT_NAME="$(cmake_get_project_name ".")"; then
        info "Detected project name from CMake: $PROJECT_NAME"
    else
        PROJECT_NAME="$(basename "$PWD")"
        warn "未检测到 project(...)，回退为目录名: $PROJECT_NAME"
    fi
fi

EXE_PATH="$BUILD_DIR/$PROJECT_NAME"

# ==========================================================
# 编译器设置
# ==========================================================
case "$COMPILER" in
    gun)
        export CC=gcc
        export CXX=g++
        GENERATOR="Unix Makefiles"
        ;;
    clang)
        export CC=clang
        export CXX=clang++
        GENERATOR="Ninja"
        ;;
    *)
        die "未知编译器: $COMPILER (使用 gun / clang)"
        ;;
esac

info "Compiler: $CXX"
info "Build type: $BUILD_TYPE"

# ==========================================================
# 编译器 / 构建类型变化检测
# ==========================================================
MARK_FILE="$BUILD_DIR/compiler.txt"
BUILD_TYPE_FILE="$BUILD_DIR/build_type.txt"
needs_clean=false

if [[ -d "$BUILD_DIR" ]]; then
    [[ -f "$MARK_FILE" ]] && [[ "$(cat "$MARK_FILE")" != "$COMPILER" ]] && needs_clean=true
    [[ -f "$BUILD_TYPE_FILE" ]] && [[ "$(cat "$BUILD_TYPE_FILE")" != "$BUILD_TYPE" ]] && needs_clean=true
    [[ "$needs_clean" == true ]] && warn "配置变更，清理 build 目录" && rm -rf "$BUILD_DIR"
fi

mkdir -p "$BUILD_DIR"
echo "$COMPILER" > "$MARK_FILE"
echo "$BUILD_TYPE" > "$BUILD_TYPE_FILE"

# ==========================================================
# CMake 配置 & 构建
# ==========================================================
info "${PURPLE_B}[1/3] CMake Configure${RESET}"
configure_start=$(date +%s%3N)
cmake -B "$BUILD_DIR" -G "$GENERATOR" \
      -DCMAKE_BUILD_TYPE="$BUILD_TYPE"
configure_end=$(date +%s%3N)
configure_duration=$(awk "BEGIN {print ($configure_end - $configure_start) / 1000}")
info "${BLUE}Configure finished in ${configure_duration}s.${RESET}"

info "${PURPLE_B}[2/3] Build${RESET}"
build_start=$(date +%s%3N)
cmake --build "$BUILD_DIR" || handle_error "Compilation failed."
build_end=$(date +%s%3N)
build_duration=$(awk "BEGIN {print ($build_end - $build_start) / 1000}")
info "${BLUE}Compilation finished in ${build_duration}s.${RESET}"


# ==========================================================
# 运行 / 调试
# ==========================================================
if [[ ! -f "$EXE_PATH" ]]; then
    die "未找到可执行文件: $EXE_PATH"
fi

if [[ "$BUILD_TYPE" == "Debug" ]]; then
    require_cmd gdb
    info "${PURPLE_B}[3/3] Debug (GDB)${RESET}"
    echo "======================================================================="
    gdb "$EXE_PATH"
    echo "======================================================================="
else
    info "${PURPLE_B}[3/3] Run Executable${RESET}"
    echo "======================================================================="
    "$EXE_PATH"
    echo "======================================================================="
fi
