# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction

import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

# ESP32 SPI
from adafruit_espatcontrol import (
    adafruit_espatcontrol,
    adafruit_espatcontrol_wifimanager,
)


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Debug Level
# Change the Debug Flag if you have issues with AT commands
debugflag = False

if board.board_id == "challenger_rp2040_wifi":
    RX = board.ESP_RX
    TX = board.ESP_TX
    resetpin = DigitalInOut(board.WIFI_RESET)
    rtspin = False
    uart = busio.UART(TX, RX, baudrate=11520, receiver_buffer_size=2048)
    esp_boot = DigitalInOut(board.WIFI_MODE)
    esp_boot.direction = Direction.OUTPUT
    esp_boot.value = True
    status_light = None
    pixel_pin = board.NEOPIXEL
    num_pixels = 1
else:
    RX = board.ESP_TX
    TX = board.ESP_RX
    resetpin = DigitalInOut(board.ESP_WIFI_EN)
    rtspin = DigitalInOut(board.ESP_CTS)
    uart = busio.UART(TX, RX, timeout=0.1)
    esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
    esp_boot.direction = Direction.OUTPUT
    esp_boot.value = True
    status_light = None
    pixel_pin = board.A1
    num_pixels = 16

print("ESP AT commands")
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)
wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(esp, secrets, status_light)


DATA_SOURCE = "https://api.thingspeak.com/channels/1417/feeds.json?results=1"
DATA_LOCATION = ["feeds", 0, "field2"]


# Setup and Clear neopixels
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3)
pixels.fill(0)

# we'll save the value in question
last_value = value = None

while True:
    try:
        print("Fetching json from", DATA_SOURCE)
        response = wifi.get(DATA_SOURCE)
        print(response.json())
        value = response.json()
        for key in DATA_LOCATION:
            value = value[key]
            print(value)
        response.close()
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        continue

    if not value:
        continue
    if last_value != value:
        color = int(value[1:], 16)
        red = color >> 16 & 0xFF
        green = color >> 8 & 0xFF
        blue = color & 0xFF
        gamma_corrected = fancy.gamma_adjust(fancy.CRGB(red, green, blue)).pack()
        print(
            "Setting LED To: G:{0},R:{1},B:{2},Gamma:{3}".format(
                green, red, blue, gamma_corrected
            )
        )
        pixels.fill(gamma_corrected)
        last_value = value
    response = None
    time.sleep(60)
