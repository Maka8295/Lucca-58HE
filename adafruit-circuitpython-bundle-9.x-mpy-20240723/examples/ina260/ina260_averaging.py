# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_ina260 import INA260, AveragingCount

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
ina260 = INA260(i2c)

# Raise the averaging count to a larger number to smooth out the results
ina260.averaging_count = AveragingCount.COUNT_4
while True:
    print("Current (average count 4): %.2f" % (ina260.current))
    print("Voltage (average count 4): %.2f" % (ina260.voltage))
    print("Power   (average count 4): %.2f" % (ina260.power))

    time.sleep(1)

# The can be seen most clearly using a serial plotter. Comment out the above
# and then switch between uncommenting *one* of the two below to compare

# ina260.averaging_count = AveragingCount.COUNT_1
# while True:
#     print("%.2f, %.2f, %.2f"%(ina260.current, ina260.voltage, ina260.power))
#     time.sleep(.5)

# ina260.averaging_count = AveragingCount.COUNT_4
# while True:
#     print("%.2f, %.2f, %.2f"%(ina260.current, ina260.voltage, ina260.power))
#     time.sleep(.5)
