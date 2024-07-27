# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Demo for the FT5336. Reads all available touch input coordinates.
"""

import time
import board
import adafruit_ft5336

i2c = board.I2C()
touch = adafruit_ft5336.Adafruit_FT5336(i2c)

while True:
    t = touch.points
    print(t)
    time.sleep(0.1)
