#!/usr/bin/env bash
set -e

DEFAULT_PREFIX="/usr/local"

# 如果用户显式传 PREFIX，优先使用
if [[ -n "${PREFIX:-}" ]]; then
    INSTALL_PREFIX="$PREFIX"
else
    # 尝试从用户级和系统级读取 install.conf
    if [[ -f "$HOME/.local/lib/ok-cpp/install.conf" ]]; then
        # shellcheck source=/dev/null
        source "$HOME/.local/lib/ok-cpp/install.conf"
        INSTALL_PREFIX="$PREFIX"
    elif [[ -f "/usr/local/lib/ok-cpp/install.conf" ]]; then
        # shellcheck source=/dev/null
        source "/usr/local/lib/ok-cpp/install.conf"
        INSTALL_PREFIX="$PREFIX"
    else
        INSTALL_PREFIX="$DEFAULT_PREFIX"
    fi
fi

echo "[INFO] Uninstalling ok-cpp from $INSTALL_PREFIX"

rm -f "$INSTALL_PREFIX/bin/ok-cpp"
rm -rf "$INSTALL_PREFIX/lib/ok-cpp"

echo "[OK] ok-cpp uninstalled"
