cmake_minimum_required(VERSION 3.20)
project(heartlight_hip VERSION 0.1.0 LANGUAGES CXX)

add_library(heartlight_hip INTERFACE)
target_include_directories(heartlight_hip INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_features(heartlight_hip INTERFACE cxx_std_20)

add_executable(heartlight_hip_example examples/example.cpp)
target_link_libraries(heartlight_hip_example PRIVATE heartlight_hip)
