# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import neopixel

import adafruit_lifx

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi and API secrets are kept in secrets.py, please add them there!")
    raise

# ESP32 SPI
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

# Add your LIFX Personal Access token to secrets.py
# (to obtain a token, visit: https://cloud.lifx.com/settings)
lifx_token = secrets["lifx_token"]

# Set this to your LIFX light separator label
# https://api.developer.lifx.com/docs/selectors
lifx_light = "label:Lamp"

# Initialize the LIFX API Client
lifx = adafruit_lifx.LIFX(wifi, lifx_token)

# List all lights
lights = lifx.list_lights()

# Turn on the light
print("Turning on light...")
lifx.toggle_light(lifx_light)

# Set the light's brightness to 50%
light_brightness = 0.5
lifx.set_brightness(lifx_light, light_brightness)

# Cycle the light using the colors of the Python logo
colors = ["yellow", "blue", "white"]
for color in colors:
    print("Setting light to: ", color)
    lifx.set_color(lifx_light, power="on", color=color, brightness=light_brightness)

# Turn off the light
print("Turning off light...")
lifx.toggle_light(lifx_light)
