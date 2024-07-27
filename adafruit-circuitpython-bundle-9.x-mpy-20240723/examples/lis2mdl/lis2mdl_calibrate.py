# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Calibrate the magnetometer and print out the hard-iron calibrations """

import time
import board
import adafruit_lis2mdl

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
magnetometer = adafruit_lis2mdl.LIS2MDL(i2c)

# calibration for magnetometer X (min, max), Y and Z
hardiron_calibration = [[1000, -1000], [1000, -1000], [1000, -1000]]


def calibrate():
    start_time = time.monotonic()

    # Update the high and low extremes
    while time.monotonic() - start_time < 10.0:
        magval = magnetometer.magnetic
        print("Calibrating - X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(*magval))
        for i, axis in enumerate(magval):
            hardiron_calibration[i][0] = min(hardiron_calibration[i][0], axis)
            hardiron_calibration[i][1] = max(hardiron_calibration[i][1], axis)
    print("Calibration complete:")
    print("hardiron_calibration =", hardiron_calibration)


print("Prepare to calibrate! Twist the magnetometer around in 3D in...")
print("3...")
time.sleep(1)
print("2...")
time.sleep(1)
print("1...")
time.sleep(1)

calibrate()
