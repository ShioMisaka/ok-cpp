#!/usr/bin/env bash
set -euo pipefail

DEFAULT_PREFIX="/usr/local"
INSTALL_PREFIX=""

# ==========================================================
# 解析 PREFIX
# ==========================================================
if [[ -n "${PREFIX:-}" ]]; then
    INSTALL_PREFIX="$PREFIX"
else
    if [[ -f "$HOME/.local/lib/ok-cpp/install.conf" ]]; then
        # shellcheck source=/dev/null
        source "$HOME/.local/lib/ok-cpp/install.conf"
        INSTALL_PREFIX="${PREFIX:-}"
    elif [[ -f "/usr/local/lib/ok-cpp/install.conf" ]]; then
        # shellcheck source=/dev/null
        source "/usr/local/lib/ok-cpp/install.conf"
        INSTALL_PREFIX="${PREFIX:-}"
    else
        INSTALL_PREFIX="$DEFAULT_PREFIX"
    fi
fi

# ==========================================================
# 校验 PREFIX
# ==========================================================
if [[ -z "$INSTALL_PREFIX" ]]; then
    echo "[ERROR] Invalid install prefix"
    exit 1
fi

BIN_PATH="$INSTALL_PREFIX/bin/ok-cpp"
LIB_PATH="$INSTALL_PREFIX/lib/ok-cpp"

# ==========================================================
# XDG config 路径
# ==========================================================
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/ok-cpp"

# ==========================================================
# 是否已安装检查
# ==========================================================
if [[ ! -e "$BIN_PATH" && ! -d "$LIB_PATH" ]]; then
    echo "[WARN] ok-cpp is not installed in $INSTALL_PREFIX"
    exit 0
fi

echo "[INFO] Uninstalling ok-cpp from $INSTALL_PREFIX"

# ==========================================================
# 执行卸载（程序文件）
# ==========================================================
rm -f "$BIN_PATH"
rm -rf "$LIB_PATH"

# ==========================================================
# 删除用户配置
# ==========================================================
if [[ -d "$CONFIG_DIR" ]]; then
    rm -rf "$CONFIG_DIR"
    echo "[INFO] Removed user config: $CONFIG_DIR"
else
    echo "[INFO] No user config found"
fi

echo "[OK] ok-cpp uninstalled successfully"
