#!/usr/bin/env bash
set -e

PREFIX="${PREFIX:-/usr/local}"
INSTALL_DIR="$PREFIX/lib/okcpp"
BIN_PATH="$PREFIX/bin/ok-cpp"
CONF_FILE="$INSTALL_DIR/install.conf"
VERSION_FILE_SRC="VERSION"
VERSION_FILE_DST="$INSTALL_DIR/VERSION"

ACTION="install"
OLD_VERSION=""

# ==========================================================
# 检查 Python 版本
# ==========================================================
PYTHON_CMD=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYTHON_CMD="$cmd"
        break
    fi
done

if [[ -z "$PYTHON_CMD" ]]; then
    echo "[ERROR] Python 3.8+ is required but not found."
    echo "Please install Python 3.8 or later."
    exit 1
fi

PYTHON_VERSION="$($PYTHON_CMD --version 2>&1 | awk '{print $2}')"
PYTHON_MAJOR="${PYTHON_VERSION%%.*}"
PYTHON_MINOR="${PYTHON_VERSION#*.}"
PYTHON_MINOR="${PYTHON_MINOR%%.*}"

if [[ "$PYTHON_MAJOR" -lt 3 ]] || [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -lt 8 ]]; then
    echo "[ERROR] Python 3.8+ is required, but found $PYTHON_VERSION"
    exit 1
fi

echo "[INFO] Using Python: $PYTHON_CMD ($PYTHON_VERSION)"

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
# 检查并安装 Python 依赖
# ==========================================================
echo "[INFO] Checking Python dependencies..."

# 检查依赖是否已安装
MISSING_DEPS=()

if ! $PYTHON_CMD -c "import rich" 2>/dev/null; then
    MISSING_DEPS+=("rich")
fi

if ! $PYTHON_CMD -c "import typer" 2>/dev/null; then
    MISSING_DEPS+=("typer")
fi

if [[ ${#MISSING_DEPS[@]} -gt 0 ]]; then
    echo "[INFO] Installing missing Python dependencies: ${MISSING_DEPS[*]}"
    if command -v pip &>/dev/null; then
        pip install "${MISSING_DEPS[@]}" || {
            echo "[WARN] Failed to install dependencies via pip"
            echo "[INFO] Please install manually: pip install rich typer"
        }
    else
        echo "[WARN] pip not found. Please install dependencies manually:"
        echo "  pip install rich typer"
    fi
fi

# ==========================================================
# 执行安装 / 更新
# ==========================================================
mkdir -p "$PREFIX/bin"
mkdir -p "$INSTALL_DIR"

# 复制 Python 包（从 src/ 到 $PREFIX/lib/）
cp -r src/okcpp "$PREFIX/lib/"

# 复制入口脚本（从 src/bin/ 到 $PREFIX/bin/）
cp src/bin/ok-cpp "$PREFIX/bin/ok-cpp"
chmod +x "$PREFIX/bin/ok-cpp"

# 复制版本文件
cp "$VERSION_FILE_SRC" "$INSTALL_DIR/"

# 记录安装信息
cat > "$CONF_FILE" <<EOF
PREFIX=$PREFIX
PYTHON_CMD=$PYTHON_CMD
PYTHON_VERSION=$PYTHON_VERSION
EOF

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
