#This CMake file is a modified version of the CMakeLists for body-tracking-samples, modified for Azure Maze use.

cmake_minimum_required(VERSION 3.9.0)
cmake_policy(SET CMP0048 NEW)

project(trackhands C)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 99)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)

FIND_PACKAGE(k4a REQUIRED)
FIND_PACKAGE(k4abt REQUIRED)

if ("${CMAKE_SYSTEM_NAME}" STREQUAL "Linux")
    set(CMAKE_BUILD_RPATH "\$ORIGIN")
endif()

if ("${CMAKE_C_COMPILER_ID}" STREQUAL "GNU" OR "${CMAKE_C_COMPILER_ID}" STREQUAL "Clang")
    set(CMAKE_CXX_VISIBILITY_PRESET hidden)
    set(CMAKE_C_VISIBILITY_PRESET hidden)
    set(CMAKE_VISIBILITY_INLINES_HIDDEN 1)
endif()

if ("${CMAKE_C_COMPILER_ID}" STREQUAL "GNU" OR "${CMAKE_C_COMPILER_ID}" STREQUAL "Clang")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,--as-needed,-rpath-link=${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,--as-needed,-rpath-link=${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
endif()



add_executable(trackhands tracker.c)


target_include_directories(trackhands PRIVATE ../libs/k4abt_headers)
target_link_libraries(trackhands PRIVATE
    m
    k4a
    k4abt
    window_controller_3d::window_controller_3d
    glfw::glfw
    )
