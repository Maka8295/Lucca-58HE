# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example lights up the third NeoPixel while button A is being pressed, and lights up the
eighth NeoPixel while button B is being pressed."""
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.3
cp.pixels.fill((0, 0, 0))  # Turn off the NeoPixels if they're on!

while True:
    if cp.button_a:
        cp.pixels[2] = (0, 255, 0)
    else:
        cp.pixels[2] = (0, 0, 0)

    if cp.button_b:
        cp.pixels[7] = (0, 0, 255)
    else:
        cp.pixels[7] = (0, 0, 0)
