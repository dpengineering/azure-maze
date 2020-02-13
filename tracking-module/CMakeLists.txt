cmake_minimum_required(VERSION 2.6.0)

project(trackhands C)

FIND_PACKAGE(k4a REQUIRED)
FIND_PACKAGE(k4abt REQUIRED)


add_executable(trackhands tracker.c)
target_link_libraries(trackhands m)
target_link_libraries(trackhands k4a)
target_link_libraries(trackhands k4abt)
