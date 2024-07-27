# SPDX-FileCopyrightText: 2021 Sandy Macdonald, David Glaude, James Carr
# SPDX-License-Identifier: MIT

"""
Example to display a rainbow animation on the 5x5 RGB Matrix Breakout.

Usage:
Rename this file code.py and pop it on your Raspberry Pico's
CIRCUITPY drive.

This example is for use on the Pico Explorer Base or other board that use the same SDA/SCL pin.

Author(s): Sandy Macdonald, David Glaude, James Carr
"""

import time
import math
import busio
import board

from adafruit_is31fl3731.rgbmatrix5x5 import RGBmatrix5x5 as Display


def hsv_to_rgb(hue, sat, val):
    # pylint: disable=too-many-return-statements
    """
    Convert HSV colour to RGB

    :param hue: hue; 0.0-1.0
    :param sat: saturation; 0.0-1.0
    :param val: value; 0.0-1.0
    """

    if sat == 0.0:
        return val, val, val

    i = int(hue * 6.0)

    p = val * (1.0 - sat)
    f = (hue * 6.0) - i
    q = val * (1.0 - sat * f)
    t = val * (1.0 - sat * (1.0 - f))

    i %= 6

    if i == 0:
        return val, t, p
    if i == 1:
        return q, val, p
    if i == 2:
        return p, val, t
    if i == 3:
        return p, q, val
    if i == 4:
        return t, p, val
    if i == 5:
        return val, p, q

    # Will never reach here but it keeps pylint happier
    return val, val, val


# Create the I2C bus on a Pico Explorer Base
i2c = busio.I2C(board.GP5, board.GP4)

# Set up 5x5 RGB matrix Breakout
display = Display(i2c)


def test_pixels(r, g, b):
    # Draw each row from left to right, top to bottom
    for y in range(0, 5):
        for x in range(0, 5):
            display.fill(0)  # Clear display
            display.pixelrgb(x, y, r, g, b)
            time.sleep(0.05)


def test_rows(r, g, b):
    # Draw full rows from top to bottom
    for y in range(0, 5):
        display.fill(0)  # Clear display
        for x in range(0, 5):
            display.pixelrgb(x, y, r, g, b)
        time.sleep(0.2)


def test_columns(r, g, b):
    # Draw full columns from left to right
    for x in range(0, 5):
        display.fill(0)  # Clear display
        for y in range(0, 5):
            display.pixelrgb(x, y, r, g, b)
        time.sleep(0.2)


def test_rainbow_sweep():
    step = 0

    for _ in range(100):
        for y in range(0, 5):
            for x in range(0, 5):
                pixel_hue = (x + y + (step / 20)) / 8
                pixel_hue = pixel_hue - int(pixel_hue)
                pixel_hue += 0
                pixel_hue = pixel_hue - math.floor(pixel_hue)

                rgb = hsv_to_rgb(pixel_hue, 1, 1)

                display.pixelrgb(
                    x, y, int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
                )

        time.sleep(0.01)
        step += 3


while True:
    test_pixels(64, 0, 0)  # RED
    test_pixels(0, 64, 0)  # GREEN
    test_pixels(0, 0, 64)  # BLUE
    test_pixels(64, 64, 64)  # WHITE

    test_rows(64, 0, 0)  # RED
    test_rows(0, 64, 0)  # GREEN
    test_rows(0, 0, 64)  # BLUE
    test_rows(64, 64, 64)  # WHITE

    test_columns(64, 0, 0)  # RED
    test_columns(0, 64, 0)  # GREEN
    test_columns(0, 0, 64)  # BLUE
    test_columns(64, 64, 64)  # WHITE

    test_rainbow_sweep()
