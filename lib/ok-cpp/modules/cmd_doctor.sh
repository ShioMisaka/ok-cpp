#!/usr/bin/env bash
# cmd_doctor.sh - ok-cpp doctor
set -euo pipefail

# ==========================================================
# 基础路径 & 公共函数
# ==========================================================
ROOT_DIR="${OK_CPP_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
COMMON="$ROOT_DIR/lib/ok-cpp/common.sh"

# shellcheck source=/dev/null
source "$COMMON"

# ==========================================================
# 内部工具函数
# ==========================================================
print_section() {
    echo
    echo "== $1 =="
}

check_cmd() {
    local name="$1"
    local cmd="$2"

    if command -v "$cmd" &>/dev/null; then
        local version
        version="$("$cmd" --version 2>/dev/null | head -n 1)"
        ok "✔ $name: $version"
        return 0
    else
        warn "✘ $name: not found"
        return 1
    fi
}

# ==========================================================
# Doctor 开始
# ==========================================================
info "ok-cpp doctor - environment check"

# ----------------------------------------------------------
# 编译器
# ----------------------------------------------------------
print_section "C++ Compilers"

has_compiler=false

if check_cmd "GCC (g++)" g++; then
    has_compiler=true
fi

if check_cmd "Clang (clang++)" clang++; then
    has_compiler=true
fi

if [[ "$has_compiler" == false ]]; then
    warn "No C++ compiler found (install g++ or clang++)"
fi

# ----------------------------------------------------------
# 构建工具
# ----------------------------------------------------------
print_section "Build Tools"

check_cmd "CMake" cmake
check_cmd "Ninja" ninja || warn "Ninja not found (optional, recommended)"

# ----------------------------------------------------------
# 调试工具
# ----------------------------------------------------------
print_section "Debug Tools"

check_cmd "GDB" gdb || warn "GDB not found (required for Debug mode)"

# ----------------------------------------------------------
# Qt (当前唯一模板依赖)
# ----------------------------------------------------------
print_section "Qt (Template Dependency)"

if command -v qmake &>/dev/null; then
    ok "✔ Qt (qmake): $(qmake --version | head -n 1)"
elif command -v qtpaths &>/dev/null; then
    ok "✔ Qt (qtpaths): detected"
else
    warn "✘ Qt not found (required for Qt templates)"
    info "  Hint: install qtbase-dev / qt6-base-dev"
fi

# ----------------------------------------------------------
# 总结
# ----------------------------------------------------------
echo
info "Doctor check finished."
info "If something is missing, install it and re-run: ok-cpp doctor"
