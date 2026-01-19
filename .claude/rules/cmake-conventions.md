# CMake 约定规则

ok-cpp 项目模板的 CMakeLists.txt 编写约定。

## 基本结构

每个模板的 CMakeLists.txt 应遵循以下结构：

```cmake
cmake_minimum_required(VERSION 3.15)
project(okcpp_template)  # 会被 create_project() 自动替换

# 设置项目根目录变量
set(PROJECT_ROOT_DIR ${CMAKE_CURRENT_LIST_DIR})

# C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 输出目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# 构建类型配置
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# 编译选项
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-g -O0)
    add_definitions(-DDEBUG_MODE)
else()
    add_compile_options(-O3)
endif()

# <<< Import SDK Package <<<
# 在这里添加外部依赖的 find_package
# >>> Import SDK Package >>>

# 源文件
add_executable(${PROJECT_NAME} main.cpp)

# 链接库
# target_link_libraries(${PROJECT_NAME} ...)
```

## 必需元素

### 1. project() 声明

```cmake
project(okcpp_template)
```

- 必须包含，用于 `core/builder.py:get_cmake_project_name()` 解析
- 使用 `okcpp_template` 作为占位符名称
- 会在 `mkp` 命令执行时被自动替换为实际项目名

### 2. PROJECT_ROOT_DIR 变量

```cmake
set(PROJECT_ROOT_DIR ${CMAKE_CURRENT_LIST_DIR})
```

- 设置项目根目录变量
- 可在源代码中通过 `PROJECT_ROOT_DIR` 引用项目根路径
- 示例：`#define PROJECT_ROOT_DIR "@PROJECT_ROOT_DIR@"`

### 3. 输出目录配置

```cmake
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
```

- 确保可执行文件输出到 `build/` 目录
- 与 `core/builder.py:get_executable_path()` 的路径查找逻辑保持一致

## 外部依赖约定

使用标记注释包裹外部依赖配置：

```cmake
# <<< Import SDK Package <<<
find_package(Qt6 COMPONENTS Core Widgets REQUIRED)
find_package(OpenCV REQUIRED)
# >>> Import SDK Package >>>
```

- 使用 `# <<< Import SDK Package <<<` 和 `# >>> Import SDK Package >>>` 标记
- 方便用户识别和修改依赖部分
- 保持代码结构的清晰性

## 构建类型支持

### Debug 模式
- 编译选项：`-g -O0`
- 预处理器定义：`DEBUG_MODE`
- 用途：支持 GDB 调试

### Release 模式
- 编译选项：`-O3`
- 无预处理器定义
- 用途：优化性能

## 模板示例

### 基础模板 (default)

```cmake
cmake_minimum_required(VERSION 3.15)
project(okcpp_template)

set(PROJECT_ROOT_DIR ${CMAKE_CURRENT_LIST_DIR})
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-g -O0)
    add_definitions(-DDEBUG_MODE)
else()
    add_compile_options(-O3)
endif()

add_executable(${PROJECT_NAME} main.cpp)
```

### Qt 模板

```cmake
cmake_minimum_required(VERSION 3.15)
project(okcpp_template)

set(PROJECT_ROOT_DIR ${CMAKE_CURRENT_LIST_DIR})
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-g -O0)
    add_definitions(-DDEBUG_MODE)
else()
    add_compile_options(-O3)
endif()

# <<< Import SDK Package <<<
find_package(Qt6 COMPONENTS Core Widgets REQUIRED)
# >>> Import SDK Package >>>

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} Qt6::Core Qt6::Widgets)
```

## 修改现有模板时的注意事项

1. **保持 project() 声明** - 不要删除或重命名 `project(okcpp_template)`

2. **不要破坏路径查找逻辑** - 确保可执行文件输出到 `build/`

3. **使用标记注释** - 添加新依赖时放在 `# <<< Import SDK Package <<<` 区域内

4. **测试两种构建类型** - 修改后测试 `ok-cpp run -b Debug` 和 `ok-cpp run -b Release`
