# SPDX-FileCopyrightText: 2023 DJDevon3
# SPDX-License-Identifier: MIT
# Pi Pico & Picowbell with SSD1306 display & BME280 sensor
# Coded for Circuit Python 8.1

import time
import board
import displayio

# Compatibility with both CircuitPython 8.x.x and 9.x.x.
# Remove after 8.x.x is no longer a supported release.
try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

import busio
import terminalio
from adafruit_display_text import label
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_displayio_ssd1306 as ssd1306

# Reinitalizes display upon any soft reboot or hard reset
displayio.release_displays()

# Pi Pico RP2040 I2C0 bus initialization (SSD1306 display)
i2c0 = busio.I2C(board.GP3, board.GP2)
# Pi Pico RP2040 I2C1 bus initialization (temp sensor from Stemma port)
i2c1 = busio.I2C(board.GP5, board.GP4)
# i2c = board.I2C()  # other boards use board.SCL and board.SDA

# Initialize BME280 sensor
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c1)

# Configure display size
ssd_width = 128
ssd_height = 32

# Ensure the physical address of your SSD1306 is set here:
ssd_bus = I2CDisplayBus(i2c0, device_address=0x3C)
display = ssd1306.SSD1306(ssd_bus, width=ssd_width, height=ssd_height)

# Manually set your sea_level_pressure to your area
# This can change houly, lookup NOAA data or automate it.
# On a normal sunny day it's generally 1013-1015
bme280.sea_level_pressure = 1013.4
# If you live at 0 sea level this is a nice workaround
# bme280.sea_level_pressure = bme280.pressure

# Quick Colors for Labels
TEXT_BLACK = 0x000000
TEXT_BLUE = 0x0000FF
TEXT_CYAN = 0x00FFFF
TEXT_GRAY = 0x8B8B8B
TEXT_GREEN = 0x00FF00
TEXT_LIGHTBLUE = 0x90C7FF
TEXT_MAGENTA = 0xFF00FF
TEXT_ORANGE = 0xFFA500
TEXT_PURPLE = 0x800080
TEXT_RED = 0xFF0000
TEXT_WHITE = 0xFFFFFF
TEXT_YELLOW = 0xFFFF00

# Text labels for display
hello_label = label.Label(terminalio.FONT)
hello_label.anchor_point = (0.0, 0.0)
hello_label.anchored_position = (0, 0)
hello_label.scale = 1
hello_label.color = TEXT_WHITE

temp_label = label.Label(terminalio.FONT)
temp_label.anchor_point = (0.0, 0.0)
temp_label.anchored_position = (0, 10)
temp_label.scale = 1
temp_label.color = TEXT_WHITE

humidity_label = label.Label(terminalio.FONT)
humidity_label.anchor_point = (0.0, 0.0)
humidity_label.anchored_position = (0, 20)
humidity_label.scale = 1
humidity_label.color = TEXT_WHITE

pressure_label = label.Label(terminalio.FONT)
pressure_label.anchor_point = (1.0, 1.0)
pressure_label.anchored_position = (ssd_width, 10)
pressure_label.scale = 1
pressure_label.color = TEXT_WHITE

# Create DisplayIO Group Layer
layer1 = displayio.Group()
layer1.append(hello_label)
layer1.append(temp_label)
layer1.append(humidity_label)
layer1.append(pressure_label)
display.root_group = layer1

while True:
    # Convert temp C to F
    temperature = f"{bme280.temperature * 1.8 + 32:.1f}"

    # Displays labels on the SSD1306 display
    hello_label.text = "Pico W SSD1306"
    temp_label.text = temperature
    humidity_label.text = f"{bme280.relative_humidity:.0f}"
    pressure_label.text = f"{bme280.pressure:.0f}"

    # Prints Serial Data to REPL console (good for debugging)
    print(f"\nTemperature: {temperature} F")
    print("Humidity: %0.1f %%" % bme280.relative_humidity)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    print("Altitude = %0.2f meters" % bme280.altitude)
    time.sleep(2)
