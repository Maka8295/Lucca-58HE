# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from rainbowio import colorwheel

from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT
import adafruit_is31fl3741

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
is31 = Adafruit_RGBMatrixQT(i2c, allocate=adafruit_is31fl3741.PREFER_BUFFER)
is31.set_led_scaling(0xFF)
is31.global_current = 0xFF
# print("Global current is: ", is31.global_current)
is31.enable = True
# print("Enabled? ", is31.enable)

wheeloffset = 0
while True:
    for y in range(9):
        for x in range(13):
            is31.pixel(x, y, colorwheel((y * 13 + x) * 2 + wheeloffset))
    wheeloffset += 1
    is31.show()
