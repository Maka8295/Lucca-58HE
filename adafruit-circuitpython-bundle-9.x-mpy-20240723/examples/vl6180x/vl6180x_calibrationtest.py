# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Demo of calibrating the part to part range offset per Application Note 4545
# for the VL6180X sensor

import time

import board
import busio

import adafruit_vl6180x


# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor instance, with explicit offset of 0 to clear the system offset
sensor = adafruit_vl6180x.VL6180X(i2c, offset=0)

# Place a target at 50mm away from VL6180X Collect a number of range measurements
# with the target in place and calculate mean of the range results.  For a
# reliable measurement, take at least 10 measurements.
measurements = []
for msmt in range(10):
    range_mm = sensor.range
    measurements.append(range_mm)
    time.sleep(1.0)
average_msmt = sum(measurements) / 10

# Calculate the offset required:
calibration_offset = 50 - average_msmt

# Apply offset
sensor.offset = calibration_offset
