cmake_minimum_required(VERSION 3.20)

project(test2_qt)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 开启自动 moc 生成
set(CMAKE_AUTOMOC ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/build)

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

find_package(Qt5 5.14.2 REQUIRED COMPONENTS Widgets)

# >>> Import SDK Package >>>

# 头文件
set(HEAD_FILE
    include/MainWindow.h
)

# 源文件
set(SRC_FILE 
    main.cpp
    src/MainWindow.cpp
)

# 添加可执行文件
add_executable(${PROJECT_NAME} ${HEAD_FILE} ${SRC_FILE})

# 链接第三方库
target_link_libraries(${PROJECT_NAME}  Qt5::Core Qt5::Widgets)

# 包含目录（不需要加上第三方库的包含）
target_include_directories(${PROJECT_NAME} PUBLIC include)