# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example for getting touch data from an FT6206 or FT6236 capacitive
touch driver, over I2C
"""

import time
import busio
import board
import adafruit_focaltouch

# Create library object (named "ft") using a Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)

ft = adafruit_focaltouch.Adafruit_FocalTouch(i2c, debug=False)

while True:
    # if the screen is being touched print the touches
    if ft.touched:
        print(ft.touches)
    else:
        print("no touch")

    time.sleep(0.15)
