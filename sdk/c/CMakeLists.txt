cmake_minimum_required(VERSION 3.16)
project(heartlight_synaptic C)

add_library(heartlight_synaptic STATIC src/heartlight_synaptic.c)
target_include_directories(heartlight_synaptic PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
set_target_properties(heartlight_synaptic PROPERTIES C_STANDARD 11 C_STANDARD_REQUIRED YES)

add_executable(heartlight_synaptic_test tests/synaptic_test.c)
target_link_libraries(heartlight_synaptic_test PRIVATE heartlight_synaptic m)
