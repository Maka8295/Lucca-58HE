# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_icm20x import ICM20948

cycles = 200
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
icm = ICM20948(i2c)

# Cycle between two data rates
# Best viewed in the Mu serial plotter where you can see how
# the data rate affects the resolution of the data
while True:
    icm.accelerometer_data_rate_divisor = 0  # minimum
    print("Data Rate:", icm.accelerometer_data_rate)
    time.sleep(2)
    for i in range(cycles):
        print(icm.acceleration)

    icm.accelerometer_data_rate_divisor = 4095  # maximum
    print("Data Rate:", icm.accelerometer_data_rate)
    time.sleep(2)
    for i in range(cycles):
        print(icm.acceleration)
