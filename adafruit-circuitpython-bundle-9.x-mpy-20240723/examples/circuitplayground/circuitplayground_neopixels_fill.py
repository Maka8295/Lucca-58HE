# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example lights up all the NeoPixel LEDs red."""
from adafruit_circuitplayground import cp

while True:
    cp.pixels.fill((50, 0, 0))
