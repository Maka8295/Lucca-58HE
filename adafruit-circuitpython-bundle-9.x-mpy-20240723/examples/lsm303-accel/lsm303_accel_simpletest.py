# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display accelerometer data once per second """

import time
import board
import adafruit_lsm303_accel

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_lsm303_accel.LSM303_Accel(i2c)

while True:
    acc_x, acc_y, acc_z = sensor.acceleration

    print(
        "Acceleration (m/s^2): ({0:10.3f}, {1:10.3f}, {2:10.3f})".format(
            acc_x, acc_y, acc_z
        )
    )
    print("")
    time.sleep(1.0)
