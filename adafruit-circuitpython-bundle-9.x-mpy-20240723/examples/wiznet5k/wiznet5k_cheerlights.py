# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from digitalio import DigitalInOut

import adafruit_connection_manager
import adafruit_requests

import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K

cs = DigitalInOut(board.D10)
spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs)

# Initialize a requests session
pool = adafruit_connection_manager.get_radio_socketpool(eth)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(eth)
requests = adafruit_requests.Session(pool, ssl_context)

DATA_SOURCE = "http://api.thingspeak.com/channels/1417/feeds.json?results=1"
DATA_LOCATION = ["feeds", 0, "field2"]

# neopixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)
pixels.fill(0)

attempts = 3  # Number of attempts to retry each request
failure_count = 0
response = None

# we'll save the value in question
last_value = value = None

while True:
    try:
        print("Fetching json from", DATA_SOURCE)
        response = requests.get(DATA_SOURCE)
        print(response.json())
        value = response.json()
        for key in DATA_LOCATION:
            value = value[key]
            print(value)
        response.close()
        failure_count = 0
    except AssertionError as error:
        print("Request failed, retrying...\n", error)
        failure_count += 1
        if failure_count >= attempts:
            raise AssertionError(
                "Failed to resolve hostname, \
                                  please check your router's DNS configuration."
            ) from error
        continue
    if not value:
        continue
    if last_value != value:
        color = int(value[1:], 16)
        red = color >> 16 & 0xFF
        green = color >> 8 & 0xFF
        blue = color & 0xFF
        gamma_corrected = fancy.gamma_adjust(fancy.CRGB(red, green, blue)).pack()

        pixels.fill(gamma_corrected)
        last_value = value
    response = None
    time.sleep(60)
