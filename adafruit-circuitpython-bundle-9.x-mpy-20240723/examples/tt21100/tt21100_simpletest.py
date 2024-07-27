# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
Example for getting touch data from a TT21100 capacitive touch driver over I2C
"""

import time
import busio
import board
import adafruit_tt21100

# Create library object (named "tt") using a Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)

tt = adafruit_tt21100.TT21100(i2c)

while True:
    # if the screen is being touched print the touches
    if tt.touched:
        print(tt.touches)

    time.sleep(0.15)
