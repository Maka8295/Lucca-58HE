# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import adafruit_guvx_i2c

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_guvx_i2c.GUVB_C31SM(i2c)

# Check advanced example for more settings, start with lowest range
sensor.range = 1

while True:
    print("UVB:", sensor.uvb)
    time.sleep(1)
