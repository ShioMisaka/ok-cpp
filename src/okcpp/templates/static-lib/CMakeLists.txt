cmake_minimum_required(VERSION 3.20)

project(okcpp_template)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/build)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/build)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/build)

# 设置当前项目的根目录
set(PROJECT_ROOT_DIR ${CMAKE_CURRENT_LIST_DIR})

# 如果没有指定构建类型，默认为 Release
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# Debug 模式配置
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    message(STATUS "Building in Debug mode")
    # 添加调试符号，禁用优化
    set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")
    add_compile_definitions(DEBUG_MODE)

    # 针对不同编译器的额外调试选项
    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        add_compile_options(-Wall -Wextra -pedantic)
    endif()
else()
    message(STATUS "Building in Release mode")
    # Release 优化
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif()

# <<< Import SDK Package <<<

# >>> Import SDK Package >>>

# 静态库目标
add_library(${PROJECT_NAME} STATIC
    src/mylib.cpp
)

# 公共头文件导出
target_include_directories(${PROJECT_NAME} PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# 编译选项（库本身）
target_compile_options(${PROJECT_NAME} PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra>
)

# 测试可执行文件
add_executable(${PROJECT_NAME}_test
    test/main.cpp
)

# 链接库
target_link_libraries(${PROJECT_NAME}_test PRIVATE ${PROJECT_NAME})

# 确保库先构建
add_dependencies(${PROJECT_NAME}_test ${PROJECT_NAME})
