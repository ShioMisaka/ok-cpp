# ok-cpp

一款基于CMake的轻量级Linux C++开发环境与模板管理器。

`ok-cpp`旨在通过CMake帮助您快速创建、构建、运行和调试小型C++项目。
它特别适用于C++学习、演示测试以及管理多个小型示例项目。

---

## 功能亮点

- 🚀 CMake项目一键构建运行
- 📁 带模板的项目生成器（`mkp`）
- 🧩 模板系统（默认/Qt，可扩展）
- 🧪 调试与发布模式
- 🩺 环境检测工具`doctor`
- 📦 支持用户级与系统级安装

---

## 安装指南

安装前请赋予脚本可执行权限：

```bash
chmod +x ./install.sh
chmod +x ./uninstall.sh
```

## 系统级安装
```bash
sudo ./install.sh
```

此命令将 `ok-cpp` 安装至 `/usr/local`。

## 用户级安装（无需 sudo）
```bash
PREFIX=$HOME/.local ./install.sh
```

确保 `~/.local/bin` 位于 `PATH` 环境变量中：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

建议将此行添加至 `~/.bashrc` 或 `~/.zshrc`。

---

## 卸载
```bash
./uninstall.sh
```

若使用自定义前缀安装：

```bash
PREFIX=$HOME/.local ./uninstall.sh
```

## 使用指南
### 构建与运行

```bash
ok-cpp run                  # 在当前目录运行项目
ok-cpp run path/project     # 按路径运行项目
ok-cpp run project_name     # 按名称运行项目（支持搜索）
```

### 运行选项

```bash
ok-cpp run -d
ok-cpp run --debug          # 调试模式（GDB）

ok-cpp run -c clang         # 使用 clang / clang++
ok-cpp run -c gun           # 使用 gcc / g++

ok-cpp run -p my_project    # 覆盖项目名称
```

### 项目创建 (mkp)

#### 使用默认模板
```bash
ok-cpp mkp demos/hello
```

#### 使用 Qt 模板
```bash
ok-cpp mkp demos/qt_app -t qt
```

#### 列出可用模板
```bash
ok-cpp mkp --list
```

#### 目录名与项目名不一致
```bash
ok-cpp mkp demos/app -n my_app
```

### 环境检测

检查所需工具及依赖项是否安装：
```bash
ok-cpp doctor
```

检测内容：
- C++编译器（g++ / clang++）
- CMake
- Ninja（可选）
- GDB（调试模式所需）
- Qt（Qt模板所需）

### 版本信息
```bash
ok-cpp --version
```

### 项目结构

```txt
ok_cpp/
├── bin/
│   └── ok-cpp              # 安装入口点
├── lib/ok-pp/
│   ├── modules/            # 命令模块
│   ├── templates/          # 项目模板
│   └── common.sh           # 通用工具
├── install.sh              # 安装脚本
├── uninstall.sh            # 卸载脚本
├── VERSION                 # 版本文件
└── README.md
```

## 许可协议

本项目采用 MIT 许可证，详情见 [LICENSE](LICENSE) 文件。