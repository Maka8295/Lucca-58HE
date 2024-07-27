# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import neopixel

# Import Philips Hue Bridge
from adafruit_hue import Bridge

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

# Attempt to load bridge username and IP address from secrets.py
try:
    username = secrets["hue_username"]
    bridge_ip = secrets["bridge_ip"]
    my_bridge = Bridge(wifi, bridge_ip, username)
except:
    # Perform first-time bridge setup
    my_bridge = Bridge(wifi)
    ip = my_bridge.discover_bridge()
    username = my_bridge.register_username()
    print(
        'ADD THESE VALUES TO SECRETS.PY: \
                            \n\t"bridge_ip":"{0}", \
                            \n\t"hue_username":"{1}"'.format(
            ip, username
        )
    )
    raise

# Enumerate all lights on the bridge
my_bridge.get_lights()

# Turn on the light
my_bridge.set_light(1, on=True)

# RGB colors to Hue-Compatible HSL colors
hsl_y = my_bridge.rgb_to_hsb([255, 255, 0])
hsl_b = my_bridge.rgb_to_hsb([0, 0, 255])
hsl_w = my_bridge.rgb_to_hsb([255, 255, 255])
hsl_colors = [hsl_y, hsl_b, hsl_w]

# Set the light to Python colors!
for color in hsl_colors:
    my_bridge.set_light(1, hue=int(color[0]), sat=int(color[1]), bri=int(color[2]))
    time.sleep(5)

# Set a predefinedscene
# my_bridge.set_group(1, scene='AB34EF5')

# Turn off the light
my_bridge.set_light(1, on=False)
