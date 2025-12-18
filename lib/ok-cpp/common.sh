#!/usr/bin/env bash
# common.sh - 公共函数（颜色打印、路径处理、工具检查）
set -euo pipefail

# --- 颜色定义 ---

RED=$'\033[31m'
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
BLUE=$'\033[34m'
PURPLE=$'\033[35m'

RED_B=$'\033[1;31m'
GREEN_B=$'\033[1;32m'
YELLOW_B=$'\033[1;33m'
BLUE_B=$'\033[1;34m'
PURPLE_B=$'\033[1;35m'


RESET=$'\033[0m'


# Functions for logging
_log_prefix() { printf "%s" "$(basename "$0")"; }
ok() { printf "%b\n" "${GREEN_B}[OK]${RESET} $*"; }
info() { printf "%b\n" "${GREEN_B}[INFO]${RESET} $*"; }
warn() { printf "%b\n" "${YELLOW_B}[WARN]${RESET} $*"; }
err()  { printf "%b\n" "${RED_B}[ERR]${RESET} $*"; }
die()  { err "$*"; exit 1; }

# Convert to absolute path
abs_path() {
  # usage: abs_path <path>
  local p="$1"
  if [ -z "$p" ]; then
    printf "%s\n" ""
    return
  fi
  if [ -d "$p" ]; then
    (cd "$p" 2>/dev/null && pwd) || true
  else
    local dir
    dir="$(cd "$(dirname "$p")" 2>/dev/null && pwd)" || dir=""
    if [ -z "$dir" ]; then
      printf "%s\n" "$p"
    else
      printf "%s\n" "$dir/$(basename "$p")"
    fi
  fi
}

# require command
require_cmd() {
  for c in "$@"; do
    if ! command -v "$c" >/dev/null 2>&1; then
      die "需要命令 '$c'，但未找到。请先安装后重试。"
    fi
  done
}

# number of cpu cores fallback
nproc_or_1() {
  if command -v nproc >/dev/null 2>&1; then
    nproc
  else
    echo 1
  fi
}

handle_error() {
    echo -e "${RED}[Error] $1${RESET}"
    read -p "Press Enter to exit..."
    exit 1
}

# ==========================================================
# CMake helpers
# ==========================================================

# 从 CMakeLists.txt 中解析 project 名
# usage: cmake_get_project_name [dir]
cmake_get_project_name() {
  local dir="${1:-.}"
  local cmake_file="$dir/CMakeLists.txt"

  [[ -f "$cmake_file" ]] || return 1

  # 支持：
  # project(foo)
  # project(foo LANGUAGES CXX)
  # project(foo VERSION 1.0)
  local name
  name=$(grep -iE '^[[:space:]]*project[[:space:]]*\(' "$cmake_file" \
        | sed -E 's/^[[:space:]]*project[[:space:]]*\(([A-Za-z0-9_\-]+).*/\1/i' \
        | head -n 1)

  [[ -n "$name" ]] || return 1
  printf "%s\n" "$name"
}