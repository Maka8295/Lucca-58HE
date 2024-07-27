# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Capture an image from the camera and display it as ASCII art.

This demo is designed to run on the Kaluga, but you can adapt it
to other boards by changing the constructors for `bus` and `cam`
appropriately.

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

import busio
import board

import adafruit_ov2640

bus = busio.I2C(scl=board.CAMERA_SIOC, sda=board.CAMERA_SIOD)
cam = adafruit_ov2640.OV2640(
    bus,
    data_pins=board.CAMERA_DATA,
    clock=board.CAMERA_PCLK,
    vsync=board.CAMERA_VSYNC,
    href=board.CAMERA_HREF,
    mclk=board.CAMERA_XCLK,
    mclk_frequency=20_000_000,
    size=adafruit_ov2640.OV2640_SIZE_QQVGA,
)
cam.colorspace = adafruit_ov2640.OV2640_COLOR_YUV
cam.flip_y = True
# cam.test_pattern = True

buf = bytearray(2 * cam.width * cam.height)
chars = b" .:-=+*#%@"
remap = [chars[i * (len(chars) - 1) // 255] for i in range(256)]

width = cam.width
row = bytearray(2 * width)

sys.stdout.write("\033[2J")
while True:
    cam.capture(buf)
    for j in range(cam.height // 2):
        sys.stdout.write(f"\033[{j}H")
        for i in range(cam.width // 2):
            row[i * 2] = row[i * 2 + 1] = remap[buf[4 * (width * j + i)]]
        sys.stdout.write(row)
        sys.stdout.write("\033[K")
    sys.stdout.write("\033[J")
    time.sleep(0.05)
