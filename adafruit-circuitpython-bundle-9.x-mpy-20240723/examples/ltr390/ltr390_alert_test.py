# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# pylint:disable=unused-import
import time
import board
from adafruit_ltr390 import LTR390, UV, ALS

THRESHOLD_VALUE = 100

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
ltr = LTR390(i2c)

ltr.high_threshold = THRESHOLD_VALUE
ltr.enable_alerts(True, UV, 1)

while True:
    if ltr.threshold_passed:
        print("UV:", ltr.uvs)
        print("threshold", THRESHOLD_VALUE, "passed!")
        print("")
    else:
        print("threshold not passed yet")

    time.sleep(1)
