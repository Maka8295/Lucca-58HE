# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_tlv493d

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
tlv = adafruit_tlv493d.TLV493D(i2c)

while True:
    print("X: %s, Y: %s, Z: %s uT" % tlv.magnetic)
    time.sleep(1)
