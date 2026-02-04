# ok-cpp

一款基于CMake的轻量级Linux C++开发环境与模板管理器。

`ok-cpp`旨在通过CMake帮助您快速创建、构建、运行和调试小型C++项目。
它特别适用于C++学习、演示测试以及管理多个小型示例项目。

**使用 Python 3.8+ 实现**

---

## 功能亮点

- 🚀 CMake项目一键构建运行
- 📁 带模板的项目生成器（`mkp`）
- 🧩 模板系统（默认/Qt/静态库/动态库，可扩展）
- 🛠️ 从现有项目创建自定义模板（`build-template`）
- 🧪 调试与发布模式
- 🩺 环境检测工具`doctor`
- 📦 支持用户级与系统级安装
- 🐍 Python 实现易于扩展

---

## 环境要求

- Python 3.8 或更高版本
- C++ 编译器（g++ 或 clang++）
- CMake
- [可选] GDB 用于调试模式
- [可选] Qt 用于 Qt 模板

---

## 安装指南

### 1. 安装 Python 依赖

```bash
pip install rich typer
```

或使用 pip3：

```bash
pip3 install rich typer
```

### 2. 安装 ok-cpp

安装前请赋予脚本可执行权限：

```bash
chmod +x ./install.sh
chmod +x ./uninstall.sh
```

#### 系统级安装
```bash
sudo ./install.sh
```

此命令将 `ok-cpp` 安装至 `/usr/local`。

#### 用户级安装（无需 sudo）
```bash
PREFIX=$HOME/.local ./install.sh
```

确保 `~/.local/bin` 位于 `PATH` 环境变量中：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

建议将此行添加至 `~/.bashrc` 或 `~/.zshrc`。

### 3. 验证安装

```bash
ok-cpp --version
ok-cpp doctor
```

---

## 卸载

```bash
./uninstall.sh
```

若使用自定义前缀安装：

```bash
PREFIX=$HOME/.local ./uninstall.sh
```

---

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

#### 使用静态库模板
```bash
ok-cpp mkp demos/mylib -t static-lib
```

#### 使用动态库模板
```bash
ok-cpp mkp demos/mylib -t dynamic-lib
```

#### 列出可用模板
```bash
ok-cpp mkp --list
```

#### 目录名与项目名不一致
```bash
ok-cpp mkp demos/app -n my_app
```

### 创建自定义模板

从现有项目创建模板：

```bash
ok-cpp build-template ./my-existing-project -n my-custom-template
```

此命令会：
- 复制项目到模板目录
- 验证模板结构
- 通过构建临时项目来测试模板

使用 `--skip-validate` 跳过验证步骤：

```bash
ok-cpp build-template ./my-project -n my-template --skip-validate
```

### 删除模板

删除自定义模板：

```bash
ok-cpp delete-template my-custom-template
```

删除前会提示确认。使用 `--force` 跳过确认：

```bash
ok-cpp delete-template my-template --force
```

### 环境检测

检查所需工具及依赖项是否安装：

```bash
ok-cpp doctor
```

检测内容：
- Python 版本和依赖
- C++编译器（g++ / clang++）
- CMake
- Ninja（可选）
- GDB（调试模式所需）
- Qt（Qt模板所需）

### 配置管理

管理用户配置：

```bash
ok-cpp config show           # 显示当前配置
ok-cpp config set compiler clang   # 设置默认编译器
ok-cpp config set template qt      # 设置默认模板
ok-cpp config reset          # 重置为默认值
```

### 版本信息

```bash
ok-cpp --version
```

---

## 项目结构

```txt
ok-cpp/
├── src/
│   ├── okcpp/              # Python 包
│   │   ├── cli/            # CLI 命令（run, mkp, build-template, doctor, config）
│   │   ├── core/           # 核心逻辑（builder, template, detector）
│   │   ├── utils/          # 工具模块（log, path, config）
│   │   └── templates/      # 项目模板（default, qt, static-lib, dynamic-lib）
│   └── bin/
│       └── ok-cpp          # 入口脚本（Python）
├── install.sh              # 安装脚本（复制 src/ 到 /usr/local）
├── uninstall.sh            # 卸载脚本
├── pyproject.toml          # Python 项目配置
├── requirements.txt        # Python 依赖
├── VERSION                 # 版本文件
└── README.md
```

---

## 开发

不安装直接运行：

```bash
./src/bin/ok-cpp <命令>
```

入口脚本会自动检测是从源代码运行还是从安装位置运行。

---

## 许可协议

本项目采用 MIT 许可证，详情见 [LICENSE](LICENSE) 文件。
