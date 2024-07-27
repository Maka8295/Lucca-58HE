# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display magnetometer data once per second """

import time
import board
import adafruit_mmc56x3

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_mmc56x3.MMC5603(i2c)

while True:
    mag_x, mag_y, mag_z = sensor.magnetic
    temp = sensor.temperature

    print(
        "X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT\tTemp:{3:6.1f}*C".format(
            mag_x, mag_y, mag_z, temp
        )
    )
    print("")
    time.sleep(1.0)
