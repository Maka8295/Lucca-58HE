# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
from adafruit_lc709203f import LC709203F

print("LC709203F simple test")
print("Make sure LiPoly battery is plugged into the board!")

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = LC709203F(i2c)

print("IC version:", hex(sensor.ic_version))
while True:
    try:
        print(
            "Battery: %0.3f Volts / %0.1f %%"
            % (sensor.cell_voltage, sensor.cell_percent)
        )
    except OSError:
        print("retry reads")

    time.sleep(1)
