# SPDX-FileCopyrightText: 2023 E. A. Graham, Jr.
# SPDX-License-Identifier: MIT

import time
import board
import busio
from adafruit_is31fl3731.led_shim import LedShim as Display

i2c = busio.I2C(board.SCL, board.SDA)

# initial display if you are using Pimoroni LED SHIM
display = Display(i2c)

y = 1
for x in range(28):
    display.pixel(x, y, 255)

display.fade(fade_in=104, pause=250)

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    display.sleep(True)
