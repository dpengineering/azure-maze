#This CMake file is a modified version of the CMakeLists for body-tracking-samples, modified for Azure Maze use.

cmake_minimum_required(VERSION 3.9.0)
cmake_policy(SET CMP0048 NEW)

project(trackhands)

FIND_PACKAGE(k4a REQUIRED)
FIND_PACKAGE(k4abt REQUIRED)


add_subdirectory(libs)

add_executable(trackhands tracker.cpp)

target_include_directories(trackhands PRIVATE ../libs/k4abt_headers)
target_link_libraries(trackhands PRIVATE
    m
    k4a
    k4abt
    window_controller_3d::window_controller_3d
    glfw::glfw
    )
