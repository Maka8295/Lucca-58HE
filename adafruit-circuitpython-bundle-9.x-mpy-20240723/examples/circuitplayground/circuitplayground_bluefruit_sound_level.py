# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example prints out sound levels using the sound sensor on a Circuit Playground Bluefruit.
Try making sounds towards the board to see the values change.

NOTE: This example does NOT support Circuit Playground Express.
"""
import time
from adafruit_circuitplayground import cp

while True:
    print("Sound level:", cp.sound_level)
    time.sleep(0.1)
