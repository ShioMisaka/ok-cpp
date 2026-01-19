# Add Template Skill

向 ok-cpp 添加新的项目模板。

## 使用场景

当需要创建新的 CMake 项目模板时使用此技能。

## 模板要求

每个模板必须位于 `lib/okcpp/templates/<template_name>/` 目录下，并包含：

1. **CMakeLists.txt** (必需)
   - 必须包含 `project(...)` 声明
   - 项目名称会被 `create_project()` 函数自动替换
   - 应遵循 CMake 约定规则（见 .claude/rules/cmake-conventions.md）

2. **源文件** (至少一个)
   - main.cpp 或其他入口文件
   - 可选的 include/, src/ 等目录

## 执行步骤

1. **确定模板名称和用途**
   - 模板名称使用小写字母和下划线，如 `qt_widget`, `opencv_basic`
   - 描述模板的主要用途和依赖

2. **创建模板目录**
   ```
   mkdir -p lib/okcpp/templates/<template_name>
   cd lib/okcpp/templates/<template_name>
   ```

3. **编写 CMakeLists.txt**
   - 包含 `project(okcpp_template)` 作为占位符（会被自动替换）
   - 设置 `PROJECT_ROOT_DIR` 为 `${CMAKE_CURRENT_LIST_DIR}`
   - 配置源文件和依赖
   - 使用 `# <<< Import SDK Package <<<` 标记外部依赖区域

4. **添加源文件**
   - 创建基本的项目结构
   - 包含示例代码展示模板用途

5. **测试模板**
   ```bash
   ok-cpp mkp test_<template> -t <template_name>
   cd test_<template>
   ok-cpp run
   ```

6. **验证模板列表**
   ```bash
   ok-cpp mkp --list
   ```

## 示例

创建一个使用 OpenCV 的简单模板：

```cmake
cmake_minimum_required(VERSION 3.15)
project(okcpp_template)  # 会被自动替换

set(PROJECT_ROOT_DIR ${CMAKE_CURRENT_LIST_DIR})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# <<< Import SDK Package <<<
find_package(OpenCV REQUIRED)
# >>> Import SDK Package >>>

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
```

## 注意事项

- 模板名称必须与目录名一致
- CMakeLists.txt 中的项目名必须是 `okcpp_template` 或类似的占位符
- 如果依赖外部库，需要在 CMakeLists.txt 中正确配置 find_package
- 模板应保持简洁，避免过度复杂
