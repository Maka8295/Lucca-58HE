# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Test Each Data Rate """

# pylint: disable=no-member
import time
import board
from adafruit_lis3mdl import LIS3MDL, Rate, PerformanceMode

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = LIS3MDL(i2c)

current_rate = Rate.RATE_155_HZ
sensor.data_rate = current_rate
start_time = time.monotonic()
print("data_rate is", Rate.string[sensor.data_rate], "HZ")
print("performance_mode is", PerformanceMode.string[sensor.performance_mode])
while True:
    mag_x, mag_y, mag_z = sensor.magnetic

    print("X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(mag_x, mag_y, mag_z))

    # sleep for enough time so that we'll read the value twice per measurement
    sleep_time = 1 / (Rate.string[current_rate] * 2)
    time.sleep(sleep_time)

    # exit loop after a second to prevent hard to stop loops with short delays
    if (time.monotonic() - start_time) > 1:
        break
