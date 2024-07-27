# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT
from time import sleep
import board
from adafruit_as7341 import AS7341

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = AS7341(i2c)
sensor.flicker_detection_enabled = True

while True:
    flicker_detected = sensor.flicker_detected
    if flicker_detected:
        print("Detected a %d Hz flicker" % flicker_detected)

    sleep(0.1)
