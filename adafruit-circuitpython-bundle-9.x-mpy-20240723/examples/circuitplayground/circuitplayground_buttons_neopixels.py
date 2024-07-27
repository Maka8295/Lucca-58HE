# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example lights up half the NeoPixels red while button A is being pressed, and half the
NeoPixels green while button B is being pressed."""
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.3
cp.pixels.fill((0, 0, 0))  # Turn off the NeoPixels if they're on!

while True:
    if cp.button_a:
        cp.pixels[0:5] = [(255, 0, 0)] * 5
    else:
        cp.pixels[0:5] = [(0, 0, 0)] * 5

    if cp.button_b:
        cp.pixels[5:10] = [(0, 255, 0)] * 5
    else:
        cp.pixels[5:10] = [(0, 0, 0)] * 5
