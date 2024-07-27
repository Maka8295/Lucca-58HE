# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example lights up the NeoPixels on a Circuit Playground Bluefruit in response to a loud sound.
Try snapping or clapping near the board to trigger the LEDs.

NOTE: This example does NOT support Circuit Playground Express.
"""
import time
from adafruit_circuitplayground import cp

while True:
    if cp.loud_sound(sound_threshold=250):
        cp.pixels.fill((50, 0, 50))
        time.sleep(0.2)
    else:
        cp.pixels.fill((0, 0, 0))
