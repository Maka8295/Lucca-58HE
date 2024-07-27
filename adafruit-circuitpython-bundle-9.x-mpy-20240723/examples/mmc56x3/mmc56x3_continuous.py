# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display magnetometer data very quickly using the continuous data capture mode"""

import board
import adafruit_mmc56x3

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_mmc56x3.MMC5603(i2c)

sensor.data_rate = 10  # in Hz, from 1-255 or 1000
sensor.continuous_mode = True

while True:
    mag_x, mag_y, mag_z = sensor.magnetic
    print("X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(mag_x, mag_y, mag_z))
