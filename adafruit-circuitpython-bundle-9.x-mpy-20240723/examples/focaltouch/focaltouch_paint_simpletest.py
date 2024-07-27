# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Simple painting demo that draws on an Adafruit capacitive touch shield with
ILI9341 display and FT6206 captouch driver
"""

import busio
import board
import digitalio
from adafruit_rgb_display import ili9341, color565
import adafruit_focaltouch

# Create library object using our Bus I2C & SPI port
i2c = busio.I2C(board.SCL, board.SDA)
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Adafruit Metro M0 + 2.8" Capacitive touch shield
cs_pin = digitalio.DigitalInOut(board.D10)
dc_pin = digitalio.DigitalInOut(board.D9)

# Initialize display
display = ili9341.ILI9341(spi, cs=cs_pin, dc=dc_pin)
# Fill with black!
display.fill(color565(0, 0, 0))

ft = adafruit_focaltouch.Adafruit_FocalTouch(i2c)

while True:
    if ft.touched:
        ts = ft.touches
        point = ts[0]  # the shield only supports one point!
        # perform transformation to get into display coordinate system!
        y = 320 - point["y"]
        x = 240 - point["x"]
        display.fill_rectangle(x - 2, y - 2, 4, 4, color565(255, 255, 255))
