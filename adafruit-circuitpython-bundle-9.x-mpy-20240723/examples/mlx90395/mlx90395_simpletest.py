# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
from time import sleep
import board
import busio
from adafruit_mlx90395 import MLX90395


i2c = busio.I2C(board.SCL, board.SDA)
sensor = MLX90395(i2c)

while True:
    print("X:{0:5.2f}, Y:{1:5.2f}, Z:{2:5.2f} uT".format(*sensor.magnetic))
    print("")

    sleep(0.5)
