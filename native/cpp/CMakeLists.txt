cmake_minimum_required(VERSION 3.16)
project(spatialforge_native_cpp VERSION 2.4.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Optimization flags for high performance
if(MSVC)
    add_compile_options(/O2 /W4)
else()
    add_compile_options(-O3 -Wall -Wextra -pedantic)
endif()

include_directories(include)

# Shared library for Python (ctypes/cffi), Rust (bindgen), and Go (cgo)
add_library(spatialforge_core SHARED
    src/spatialforge_core.cpp
)

set_target_properties(spatialforge_core PROPERTIES
    OUTPUT_NAME "spatialforge_core"
    PREFIX "lib"
)

# Test executable
add_executable(test_spatialforge_cpp
    tests/test_spatialforge_cpp.cpp
    src/spatialforge_core.cpp
)
