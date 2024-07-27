# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from adafruit_is31fl3731.led_shim import LedShim as Display

i2c = busio.I2C(board.SCL, board.SDA)

# initial display if you are using Pimoroni LED SHIM
display = Display(i2c)

# fmt: off
# This list 28 colors from a rainbow...
rainbow = [
    (255, 0, 0), (255, 54, 0), (255, 109, 0), (255, 163, 0),
    (255, 218, 0), (236, 255, 0), (182, 255, 0), (127, 255, 0),
    (72, 255, 0), (18, 255, 0), (0, 255, 36), (0, 255, 91),
    (0, 255, 145), (0, 255, 200), (0, 255, 255), (0, 200, 255),
    (0, 145, 255), (0, 91, 255), (0, 36, 255), (18, 0, 255),
    (72, 0, 255), (127, 0, 255), (182, 0, 255), (236, 0, 255),
    (255, 0, 218), (255, 0, 163), (255, 0, 109), (255, 0, 54),
]
# fmt: on


for y in range(3):
    for x in range(28):
        display.pixel(x, y, 255)
        time.sleep(0.1)
        display.pixel(x, y, 0)

while True:
    for offset in range(28):
        for x in range(28):
            r, g, b = rainbow[(x + offset) % 28]
            display.pixelrgb(x, r, g, b)
