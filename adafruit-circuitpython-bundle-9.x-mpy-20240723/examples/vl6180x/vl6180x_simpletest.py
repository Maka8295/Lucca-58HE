# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Demo of reading the range and lux from the VL6180x distance sensor and
# printing it every second.

import time

import board
import busio

import adafruit_vl6180x


# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor instance.
sensor = adafruit_vl6180x.VL6180X(i2c)
# You can add an offset to distance measurements here (e.g. calibration)
# Swapping for the following would add a +10 millimeter offset to measurements:
# sensor = adafruit_vl6180x.VL6180X(i2c, offset=10)

# Main loop prints the range and lux every second:
while True:
    # Read the range in millimeters and print it.
    range_mm = sensor.range
    print("Range: {0}mm".format(range_mm))
    # Read the light, note this requires specifying a gain value:
    # - adafruit_vl6180x.ALS_GAIN_1 = 1x
    # - adafruit_vl6180x.ALS_GAIN_1_25 = 1.25x
    # - adafruit_vl6180x.ALS_GAIN_1_67 = 1.67x
    # - adafruit_vl6180x.ALS_GAIN_2_5 = 2.5x
    # - adafruit_vl6180x.ALS_GAIN_5 = 5x
    # - adafruit_vl6180x.ALS_GAIN_10 = 10x
    # - adafruit_vl6180x.ALS_GAIN_20 = 20x
    # - adafruit_vl6180x.ALS_GAIN_40 = 40x
    light_lux = sensor.read_lux(adafruit_vl6180x.ALS_GAIN_1)
    print("Light (1x gain): {0}lux".format(light_lux))
    # Delay for a second.
    time.sleep(1.0)
