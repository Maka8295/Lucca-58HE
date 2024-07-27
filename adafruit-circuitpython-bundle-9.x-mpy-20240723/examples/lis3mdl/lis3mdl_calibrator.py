# SPDX-FileCopyrightText: 2023 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

"""
'lis3mdl_calibrator.py' is a simple CircuitPython calibrator example for
the LIS3MDL magnetometer. The resultant offset values can be used to
compensate for 'hard iron' effects, static magnetic fields, or to orient
the sensor with the earth's magnetic field for use as a compass.

The calibrator measures the minimum and maximum values for each axis as
the sensor is moved. The values are captured over a fixed number of
samples. A middle-of-the-range calibration offset value is calculated
and reported after all samples are collected.

The sensor needs to be tumbled during the collection period in a manner
that exercises the entire range of each axis. A series of overlapping
figure-eight patterns is recommended.

This code was derived from the '9dof_calibration.py' Blinka code
authored by Melissa LeBlanc-Williams for the 'Adafruit SensorLab -
Magnetometer Calibration' learning guide (c)2020.
"""

import time
import board
import busio
from adafruit_lis3mdl import LIS3MDL

SAMPLE_SIZE = 2000

i2c = busio.I2C(board.SCL, board.SDA)
magnetometer = LIS3MDL(i2c)

while True:
    print("=" * 40)
    print("LIS3MDL MAGNETOMETER CALIBRATION")
    print("  Tumble the sensor through a series of")
    print("  overlapping figure-eight patterns")
    print(f"  for approximately {SAMPLE_SIZE/100:.0f} seconds \n")

    print("  countdown to start:", end=" ")
    for i in range(5, -1, -1):
        print(i, end=" ")
        time.sleep(1)
    print("\n  MOVE the sensor...")
    print("  >     progress     <")
    print("  ", end="")

    # Initialize the min/max values
    mag_x, mag_y, mag_z = magnetometer.magnetic
    min_x = max_x = mag_x
    min_y = max_y = mag_y
    min_z = max_z = mag_z

    for i in range(SAMPLE_SIZE):
        # Capture the samples and show the progress
        if not i % (SAMPLE_SIZE / 20):
            print("*", end="")

        mag_x, mag_y, mag_z = magnetometer.magnetic

        min_x = min(min_x, mag_x)
        min_y = min(min_y, mag_y)
        min_z = min(min_z, mag_z)

        max_x = max(max_x, mag_x)
        max_y = max(max_y, mag_y)
        max_z = max(max_z, mag_z)

        time.sleep(0.01)

    # Calculate the middle of the min/max range
    offset_x = (max_x + min_x) / 2
    offset_y = (max_y + min_y) / 2
    offset_z = (max_z + min_z) / 2

    print(
        f"\n\n  Final Calibration: X:{offset_x:6.2f} Y:{offset_y:6.2f} Z:{offset_z:6.2f} uT\n"
    )

    time.sleep(5)
