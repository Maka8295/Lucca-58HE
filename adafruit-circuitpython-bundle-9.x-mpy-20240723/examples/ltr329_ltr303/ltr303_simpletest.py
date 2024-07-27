# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
from adafruit_ltr329_ltr303 import LTR303

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

time.sleep(0.1)  # sensor takes 100ms to 'boot' on power up
ltr303 = LTR303(i2c)

while True:
    print("Visible + IR:", ltr303.visible_plus_ir_light)
    print("Infrared    :", ltr303.ir_light)
    print()
    time.sleep(0.5)  # sleep for half a second
