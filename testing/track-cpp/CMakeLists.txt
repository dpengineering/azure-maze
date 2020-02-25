# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/)

add_executable(trackhands main.cpp)

target_link_libraries(trackhands PRIVATE
    k4a
    k4abt
    )
