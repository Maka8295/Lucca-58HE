# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example lights up the first NeoPixel red."""
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.3

while True:
    cp.pixels[0] = (255, 0, 0)
