# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example lights up the NeoPixels with a rainbow swirl."""
import time
from rainbowio import colorwheel
from adafruit_circuitplayground import cp


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(cp.pixels.n):
            idx = int((i * 256 / len(cp.pixels)) + j)
            cp.pixels[i] = colorwheel(idx & 255)
        cp.pixels.show()
        time.sleep(wait)


cp.pixels.auto_write = False
cp.pixels.brightness = 0.3
while True:
    rainbow_cycle(0.001)  # rainbowcycle with 1ms delay per step
