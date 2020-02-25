# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

add_executable(trackhands main.cpp)

target_include_directories(trackhands PRIVATE ../libs/k4abt_headers)

# Dependencies of this library
target_link_libraries(trackhands PRIVATE
    k4a
    k4abt
    window_controller_3d::window_controller_3d
    glfw::glfw
    )
