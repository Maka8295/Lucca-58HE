# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_mpl115a2

i2c = busio.I2C(board.SCL, board.SDA)

mpl = adafruit_mpl115a2.MPL115A2(i2c)

while True:
    print("Pressure: {}   Temperature: {}".format(mpl.pressure, mpl.temperature))
    time.sleep(1)
