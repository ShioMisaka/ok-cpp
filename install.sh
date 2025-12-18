#!/usr/bin/env bash
set -e

PREFIX="${PREFIX:-/usr/local}"
INSTALL_DIR="$PREFIX/lib/ok-cpp"
BIN_PATH="$PREFIX/bin/ok-cpp"
CONF_FILE="$INSTALL_DIR/install.conf"
VERSION_FILE_SRC="VERSION"
VERSION_FILE_DST="$INSTALL_DIR/VERSION"

ACTION="install"
OLD_VERSION=""

# ==========================================================
# 检测是否已安装
# ==========================================================
if [[ -f "$CONF_FILE" ]]; then
    # shellcheck source=/dev/null
    source "$CONF_FILE"

    if [[ "$PREFIX" == "$PREFIX" ]]; then
        ACTION="upgrade"
        [[ -f "$VERSION_FILE_DST" ]] && OLD_VERSION="$(cat "$VERSION_FILE_DST")"
    fi
fi

NEW_VERSION="$(cat "$VERSION_FILE_SRC")"

# ==========================================================
# 输出安装信息
# ==========================================================
if [[ "$ACTION" == "upgrade" ]]; then
    echo "[INFO] Upgrading ok-cpp in $PREFIX"
    [[ -n "$OLD_VERSION" ]] && echo "[INFO] Version: $OLD_VERSION → $NEW_VERSION"
else
    echo "[INFO] Installing ok-cpp to $PREFIX"
    echo "[INFO] Version: $NEW_VERSION"
fi

# ==========================================================
# 执行安装 / 更新
# ==========================================================
mkdir -p "$PREFIX/bin"
mkdir -p "$INSTALL_DIR"

cp -r bin "$PREFIX/"
cp -r lib/ok-cpp "$PREFIX/lib/"
cp "$VERSION_FILE_SRC" "$INSTALL_DIR/"

# 记录安装信息
cat > "$CONF_FILE" <<EOF
PREFIX=$PREFIX
EOF

chmod +x "$BIN_PATH"

# ==========================================================
# 完成提示
# ==========================================================
if [[ "$ACTION" == "upgrade" ]]; then
    echo "[OK] ok-cpp upgraded successfully!"
else
    echo "[OK] ok-cpp installed successfully!"
fi

echo "Install prefix: $PREFIX"
echo "Run: ok-cpp --version"
