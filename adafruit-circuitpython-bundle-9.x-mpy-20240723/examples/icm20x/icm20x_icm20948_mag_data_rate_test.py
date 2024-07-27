# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=no-member
import time
import board
from adafruit_icm20x import MagDataRate, ICM20948

cycles = 200
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
icm = ICM20948(i2c)

# Cycle between two data rates
# Best viewed in the Mu serial plotter where you can see how
# the data rate affects the resolution of the data
while True:
    icm.magnetometer_data_rate = MagDataRate.RATE_100HZ
    for i in range(cycles):
        print(icm.magnetic)
    time.sleep(0.3)
    icm.magnetometer_data_rate = MagDataRate.RATE_10HZ
    for i in range(cycles):
        print(icm.magnetic)
    time.sleep(0.3)
