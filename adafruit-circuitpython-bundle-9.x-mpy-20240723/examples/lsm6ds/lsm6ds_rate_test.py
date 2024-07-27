# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import board

# pylint:disable=no-member,unused-import
from adafruit_lsm6ds import Rate
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS

# from adafruit_lsm6ds.lsm6ds33 import LSM6DS33 as LSM6DS
# from adafruit_lsm6ds.lsm6dso32 import LSM6DSO32 as LSM6DS
# from adafruit_lsm6ds.ism330dhcx import ISM330DHCX as LSM6DS

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = LSM6DS(i2c)

while True:
    sensor.accelerometer_data_rate = Rate.RATE_12_5_HZ
    sensor.gyro_data_rate = Rate.RATE_12_5_HZ
    for i in range(100):
        print(
            "(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f" % (sensor.acceleration + sensor.gyro)
        )
    print()

    sensor.accelerometer_data_rate = Rate.RATE_52_HZ
    sensor.gyro_data_rate = Rate.RATE_52_HZ
    for i in range(100):
        print(
            "(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f" % (sensor.acceleration + sensor.gyro)
        )
    print()

    sensor.accelerometer_data_rate = Rate.RATE_416_HZ
    sensor.gyro_data_rate = Rate.RATE_416_HZ
    for i in range(100):
        print(
            "(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f" % (sensor.acceleration + sensor.gyro)
        )
    print()
