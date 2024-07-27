# SPDX-FileCopyrightText: 2021 Sandy Macdonald
# SPDX-License-Identifier: MIT

"""
Example to display a rainbow animation on the RGB LED keys of the
Keybow 2040.

Usage:
Rename this file code.py and pop it on your Keybow 2040's
CIRCUITPY drive.

This example is for use on the Keybow 2040 only, due to the way
that the LEDs are mapped out.

Author(s): Sandy Macdonald.
"""

import time
import math
import board

from adafruit_is31fl3731.keybow2040 import Keybow2040 as Display

# pylint: disable=inconsistent-return-statements
# pylint: disable=too-many-return-statements
# pylint: disable=invalid-name


def hsv_to_rgb(hue, sat, val):
    """
    Convert HSV colour to RGB

    :param hue: hue; 0.0-1.0
    :param sat: saturation; 0.0-1.0
    :param val: value; 0.0-1.0
    """

    if sat == 0.0:
        return (val, val, val)

    i = int(hue * 6.0)

    p = val * (1.0 - sat)
    f = (hue * 6.0) - i
    q = val * (1.0 - sat * f)
    t = val * (1.0 - sat * (1.0 - f))

    i %= 6

    if i == 0:
        return (val, t, p)
    if i == 1:
        return (q, val, p)
    if i == 2:
        return (p, val, t)
    if i == 3:
        return (p, q, val)
    if i == 4:
        return (t, p, val)
    if i == 5:
        return (val, p, q)


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Set up 4x4 RGB matrix of Keybow 2040
display = Display(i2c)

step = 0

while True:
    step += 1
    for y in range(0, 4):
        for x in range(0, 4):
            pixel_hue = (x + y + (step / 20)) / 8
            pixel_hue = pixel_hue - int(pixel_hue)
            pixel_hue += 0
            pixel_hue = pixel_hue - math.floor(pixel_hue)

            rgb = hsv_to_rgb(pixel_hue, 1, 1)

            display.pixelrgb(
                x, y, int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
            )

    time.sleep(0.01)
