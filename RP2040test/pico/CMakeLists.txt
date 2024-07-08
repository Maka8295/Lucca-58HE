cmake_minimum_required(VERSION 3.13)

# Initialize the SDK based on PICO_SDK_PATH
include(pico_sdk_import.cmake)

project(blink C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

set(PICO_EXAMPLES_PATH ${PROJECT_SOURCE_DIR})

# Initialize the Raspberry Pi Pico SDK
pico_sdk_init()

# Add your source file(s)
add_executable(blink
        blink.c
        )
# Link the Pico SDK to your project
target_link_libraries(blink pico_stdlib)

# Create map/bin/hex/uf2 files
pico_add_extra_outputs(blink)

