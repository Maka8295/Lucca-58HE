# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
""" This example shows off how to use the step counter built
into the ST LSM6DS series IMUs. The steps are calculated in
the chip so you don't have to do any calculations!"""

import time
import board

# pylint:disable=no-member
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33
from adafruit_lsm6ds import Rate, AccelRange

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = LSM6DS33(i2c)

# enable accelerometer sensor @ 2G and 26 Hz
sensor.accelerometer_range = AccelRange.RANGE_2G
sensor.accelerometer_data_rate = Rate.RATE_26_HZ
# no gyro used for step detection
sensor.gyro_data_rate = Rate.RATE_SHUTDOWN

# enable the pedometer
sensor.pedometer_enable = True

while True:
    print("Steps: ", sensor.pedometer_steps)
    time.sleep(1)
