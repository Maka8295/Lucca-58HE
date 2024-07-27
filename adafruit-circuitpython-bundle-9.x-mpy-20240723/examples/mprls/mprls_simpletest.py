# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_mprls

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Simplest use, connect to default over I2C
mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)

# You can also specify both reset and eoc pins
"""
import digitalio
reset = digitalio.DigitalInOut(board.D5)
eoc = digitalio.DigitalInOut(board.D6)
mpr = adafruit_mprls.MPRLS(i2c, eoc_pin=eoc, reset_pin=reset,
                           psi_min=0, psi_max=25)
"""

while True:
    print((mpr.pressure,))
    time.sleep(1)
