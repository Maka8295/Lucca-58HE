# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_nunchuk

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
nc = adafruit_nunchuk.Nunchuk(i2c)

while True:
    x, y = nc.joystick
    ax, ay, az = nc.acceleration
    print("joystick = {},{}".format(x, y))
    print("accceleration ax={}, ay={}, az={}".format(ax, ay, az))

    if nc.buttons.C:
        print("button C")
    if nc.buttons.Z:
        print("button Z")
    time.sleep(0.5)
