#!/usr/bin/env bash
# cmd_mkp.sh - create a cmake project from template
set -euo pipefail

ROOT_DIR="${OK_CPP_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
TEMPLATES_DIR="$ROOT_DIR/lib/ok-cpp/templates"
COMMON="$ROOT_DIR/lib/ok-cpp/common.sh"

# shellcheck source=/dev/null
source "$COMMON"

# ==========================================================
# 默认值
# ==========================================================
TEMPLATE_NAME="default"
PROJECT_NAME=""
LIST_ONLY=false

load_user_config
TEMPLATE_NAME="${TEMPLATE_NAME:-default}"

# ==========================================================
# 参数解析
# ==========================================================
POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--template)
      TEMPLATE_NAME="$2"
      shift 2
      ;;
    -n|--name)
      PROJECT_NAME="$2"
      shift 2
      ;;
    -l|--list)
      LIST_ONLY=true
      shift
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

# ==========================================================
# 列出模板
# ==========================================================
if [[ "$LIST_ONLY" == true ]]; then
  info "可用模板："
  for d in "$TEMPLATES_DIR"/*; do
    [[ -d "$d" && -f "$d/CMakeLists.txt" ]] || continue
    echo "  - $(basename "$d")"
  done
  exit 0
fi

# ==========================================================
# 目标路径
# ==========================================================
[[ ${#POSITIONAL[@]} -ge 1 ]] || die "用法: ok-cpp mkp <path> [options]"
target="${POSITIONAL[0]}"

if [[ "$target" = /* ]]; then
  target_dir="$target"
else
  target_dir="$(pwd)/$target"
fi

[[ ! -e "$target_dir" ]] || die "目标已存在: $target_dir"

# ==========================================================
# 模板校验
# ==========================================================
template_dir="$TEMPLATES_DIR/$TEMPLATE_NAME"

[[ -d "$template_dir" ]] || die "模板不存在: $TEMPLATE_NAME"
[[ -f "$template_dir/CMakeLists.txt" ]] || die "模板缺少 CMakeLists.txt"

# ==========================================================
# project 名
# ==========================================================
[[ -n "$PROJECT_NAME" ]] || PROJECT_NAME="$(basename "$target_dir")"

# ==========================================================
# 创建项目
# ==========================================================
parent_dir="$(dirname "$target_dir")"
mkdir -p "$parent_dir"
cp -r "$template_dir" "$target_dir"

cmake_file="$target_dir/CMakeLists.txt"

# 强制设置 project 名
sed -i -E \
  "s|^[[:space:]]*project[[:space:]]*\\([[:space:]]*[A-Za-z0-9_\\-]+|project(${PROJECT_NAME}|I" \
  "$cmake_file"

info "已创建项目: ${YELLOW}$target_dir${RESET}"
info "Template: ${GREEN_B}$TEMPLATE_NAME${RESET}"
info "CMake project name: ${PURPLE_B}$PROJECT_NAME${RESET}"
info "下一步: cd $target && ok-cpp run 来编译运行"