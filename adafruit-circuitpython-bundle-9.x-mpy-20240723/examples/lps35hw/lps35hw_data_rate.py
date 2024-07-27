# SPDX-FileCopyrightText: 2019 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
from adafruit_lps35hw import LPS35HW, DataRate

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
lps = LPS35HW(i2c)

lps.data_rate = DataRate.ONE_SHOT
lps.take_measurement()


while True:
    print("Pressure: %.2f hPa" % lps.pressure)
    print("")
    time.sleep(1)
    print("Pressure: %.2f hPa" % lps.pressure)
    print("")
    time.sleep(1)
    print("Pressure: %.2f hPa" % lps.pressure)
    print("")
    time.sleep(1)

    # take another measurement
    lps.take_measurement()

    print("New Pressure: %.2f hPa" % lps.pressure)
    print("")
    time.sleep(1)
