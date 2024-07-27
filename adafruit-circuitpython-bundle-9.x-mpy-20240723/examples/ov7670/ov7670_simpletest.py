# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Capture an image from the camera and display it as ASCII art.

The camera is placed in YUV mode, so the top 8 bits of each color
value can be treated as "greyscale".

It's important that you use a terminal program that can interpret
"ANSI" escape sequences.  The demo uses them to "paint" each frame
on top of the prevous one, rather than scrolling.

Remember to take the lens cap off, or un-comment the line setting
the test pattern!
"""

import sys
import time

import digitalio
import busio
import board

from adafruit_ov7670 import (  # pylint: disable=unused-import
    OV7670,
    OV7670_SIZE_DIV16,
    OV7670_COLOR_YUV,
    OV7670_TEST_PATTERN_COLOR_BAR_FADE,
)

# Ensure the camera is shut down, so that it releases the SDA/SCL lines,
# then create the configuration I2C bus

with digitalio.DigitalInOut(board.D39) as shutdown:
    shutdown.switch_to_output(True)
    time.sleep(0.001)
    bus = busio.I2C(board.D24, board.D25)

cam = OV7670(
    bus,
    data0=board.PCC_D0,
    clock=board.PCC_CLK,
    vsync=board.PCC_DEN1,
    href=board.PCC_DEN2,
    mclk=board.D29,
    shutdown=board.D39,
    reset=board.D38,
)
cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_YUV
cam.flip_y = True
# cam.test_pattern = OV7670_TEST_PATTERN_COLOR_BAR_FADE

buf = bytearray(2 * cam.width * cam.height)
chars = b" .:-=+*#%@"

width = cam.width
row = bytearray(2 * width)

sys.stdout.write("\033[2J")
while True:
    cam.capture(buf)
    for j in range(cam.height):
        sys.stdout.write(f"\033[{j}H")
        for i in range(cam.width):
            row[i * 2] = row[i * 2 + 1] = chars[
                buf[2 * (width * j + i)] * (len(chars) - 1) // 255
            ]
        sys.stdout.write(row)
        sys.stdout.write("\033[K")
    sys.stdout.write("\033[J")
    time.sleep(0.05)
