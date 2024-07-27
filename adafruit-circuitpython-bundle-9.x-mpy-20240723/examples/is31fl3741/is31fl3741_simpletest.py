# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_is31fl3741

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
is31 = adafruit_is31fl3741.IS31FL3741(i2c)

is31.set_led_scaling(0xFF)  # turn on LEDs all the way
is31.global_current = 0xFF  # set current to max
is31.enable = True  # enable!

# light up every LED, one at a time
while True:
    for pixel in range(351):
        is31[pixel] = 255
        time.sleep(0.01)
        is31[pixel] = 0
