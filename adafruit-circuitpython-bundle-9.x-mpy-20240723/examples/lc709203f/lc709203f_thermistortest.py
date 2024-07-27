# SPDX-FileCopyrightText: 2021 Daniel Griswold
#
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_lc709203f import LC709203F

print("LC709203F thermistor test")
print("Make sure a thermistor is connected to the board!")

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = LC709203F(i2c)

# check your NTC thermistor datasheet for the appropriate B-Constant
sensor.thermistor_bconstant = 3950
sensor.thermistor_enable = True

print("IC version:", hex(sensor.ic_version))
while True:
    print("Cell Temperature: %0.2f C" % (sensor.cell_temperature))
    time.sleep(1)
