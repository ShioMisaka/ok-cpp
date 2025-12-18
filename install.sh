#!/usr/bin/env bash
set -e

PREFIX="${PREFIX:-/usr/local}"

echo "[INFO] Installing ok-cpp to $PREFIX"

# 目录
mkdir -p "$PREFIX/bin"
mkdir -p "$PREFIX/lib/ok-cpp"

# 拷贝文件
cp -r bin "$PREFIX/"
cp -r lib/ok-cpp "$PREFIX/lib/"
cp VERSION "$PREFIX/lib/ok-cpp/"

# 记录安装信息（关键）
cat > "$PREFIX/lib/ok-cpp/install.conf" <<EOF
PREFIX=$PREFIX
EOF

# 权限
chmod +x "$PREFIX/bin/ok-cpp"

echo "[OK] ok-cpp installed!"
echo "Install prefix: $PREFIX"
echo "Try: ok-cpp --help"
