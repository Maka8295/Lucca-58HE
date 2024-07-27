# SPDX-FileCopyrightText: 2021 Eva Herrada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import math
from os import getenv
import board
import busio
from digitalio import DigitalInOut
import displayio
from adafruit_display_shapes.rect import Rect
import adafruit_imageload
import adafruit_touchscreen

# ESP32 SPI
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager

# Import NeoPixel Library
import neopixel

# Import Adafruit IO HTTP Client
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(480, 320),
)
RED = 0xFF0000
YELLOW = 0xFF9600
ORANGE = 0xFF2800
GREEN = 0x00FF00
TEAL = 0x00FF78
CYAN = 0x00FFFF
BLUE = 0x0000FF
PURPLE = 0xB400FF
MAGENTA = 0xFF0014
WHITE = 0xFFFFFF
BLACK = 0x000000

GOLD = 0xFFDE1E
PINK = 0xF15AFF
AQUA = 0x32FFFF
JADE = 0x00FF28
AMBER = 0xFF6400

"""
colors = [None, None, None, None,
          None, None, None, None,
          GREEN, ORANGE, YELLOW, RED,
          PURPLE, BLUE, CYAN, TEAL,
          GOLD, BLACK, WHITE, MAGENTA,
          AMBER, JADE, AQUA, PINK]
"""
colors = [
    None,
    None,
    GREEN,
    PURPLE,
    GOLD,
    AMBER,
    None,
    None,
    ORANGE,
    BLUE,
    BLACK,
    JADE,
    None,
    None,
    YELLOW,
    CYAN,
    WHITE,
    AQUA,
    None,
    None,
    RED,
    TEAL,
    MAGENTA,
    PINK,
]

print(colors)
group = displayio.Group()
background, palette = adafruit_imageload.load(
    "pyportal_setter.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
)
tile_grid = displayio.TileGrid(background, pixel_shader=palette)
group.append(tile_grid)
rect = Rect(0, 0, 160, 320, fill=0x000000)
group.append(rect)
print(len(group))

# Get wifi details and more from a settings.toml file
# tokens used by this Demo: CIRCUITPY_WIFI_SSID, CIRCUITPY_WIFI_PASSWORD
#                           CIRCUITPY_AIO_USERNAME, CIRCUITPY_AIO_KEY
secrets = {}
for token in ["SSID", "PASSWORD"]:
    if getenv("CIRCUITPY_WIFI_" + token):
        secrets[token.lower()] = getenv("CIRCUITPY_WIFI_" + token)
for token in ["AIO_USERNAME", "AIO_KEY"]:
    if getenv("CIRCUITPY_" + token):
        secrets[token.lower()] = getenv("CIRCUITPY_" + token)

if not secrets:
    try:
        # Fallback on secrets.py until depreciation is over and option is removed
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in settings.toml, please add them there!")
        raise

# PyPortal ESP32 Setup
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
# Secondary (SCK1) SPI used to connect to WiFi board on Arduino Nano Connect RP2040
if "SCK1" in dir(board):
    spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
else:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

"""Use below for Most Boards"""
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
"""Uncomment below for ItsyBitsy M4"""
# status_light = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
"""Uncomment below for an externally defined RGB LED (including Arduino Nano Connect)"""
# import adafruit_rgbled
# from adafruit_esp32spi import PWMOut
# RED_LED = PWMOut.PWMOut(esp, 26)
# GREEN_LED = PWMOut.PWMOut(esp, 27)
# BLUE_LED = PWMOut.PWMOut(esp, 25)
# status_light = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED)

wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

# Set your Adafruit IO Username and Key in settings.toml
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
ADAFRUIT_IO_USER = secrets["aio_username"]
ADAFRUIT_IO_KEY = secrets["aio_key"]

# Create an instance of the Adafruit IO HTTP client
io = IO_HTTP(ADAFRUIT_IO_USER, ADAFRUIT_IO_KEY, wifi)

try:
    # Get the 'temperature' feed from Adafruit IO
    neopixel_feed = io.get_feed("neopixel")
except AdafruitIO_RequestError:
    neopixel_feed = io.create_new_feed("neopixel")

board.DISPLAY.root_group = group
print("ready")
last_color = 257
last_index = 0
while True:
    p = ts.touch_point
    if p:
        x = math.floor(p[0] / 80)
        y = math.floor(p[1] / 80)
        index = 6 * y + x
        # Used to prevent the touchscreen sending incorrect results
        if last_index == index:
            color = colors[index]
            if colors[index]:
                group[1].fill = color
                if last_color != color:
                    color_str = "#{:06x}".format(color)
                    print(color_str)
                    io.send_data(neopixel_feed["key"], color_str)
                    last_color = color
        last_index = index
    time.sleep(0.1)
