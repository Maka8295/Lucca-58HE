# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_msa3xx import MSA301

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
msa = MSA301(i2c)

msa.enable_tap_detection()

while True:
    if msa.tapped:
        print("Single Tap!")
    time.sleep(0.01)
