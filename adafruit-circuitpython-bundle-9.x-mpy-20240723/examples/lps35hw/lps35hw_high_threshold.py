# SPDX-FileCopyrightText: 2019 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_lps35hw

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
lps = adafruit_lps35hw.LPS35HW(i2c)

# You may need to adjust the threshold to something closer
# to the current pressure where the sensor is
lps.pressure_threshold = 1030

lps.high_threshold_enabled = True

while True:
    print("Pressure: %.2f hPa" % lps.pressure)
    print("Threshhold exceeded: %s" % lps.high_threshold_exceeded)
    print("")
    time.sleep(1)
