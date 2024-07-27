# SPDX-FileCopyrightText: 2019 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_lps35hw

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
lps = adafruit_lps35hw.LPS35HW(i2c)

# set the current pressure as zero hPa and make measurements
# relative to that pressure, even negative!
lps.zero_pressure()
while True:
    print("Pressure: %.2f hPa" % lps.pressure)
    print("")
    time.sleep(0.5)
