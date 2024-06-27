cmake_minimum_required(VERSION 3.13)

# Set the path to the Pico SDK
set(PICO_SDK_PATH "/home/maka/Documents/Callibration/pico-sdk")

# Include the Pico SDK
include(${PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(hallcal C CXX ASM)

# Set the C and C++ standards
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the Pico SDK
pico_sdk_init()

# Add the executable
add_executable(hallcal
    callibration.c
)

# Link the Pico SDK
target_link_libraries(hallcal pico_stdlib hardware_adc)

# Enable additional outputs (e.g. UF2)
pico_add_extra_outputs(hallcal)

