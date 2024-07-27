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

import adafruit_ov5640

print("construct bus")
bus = busio.I2C(scl=board.CAMERA_SIOC, sda=board.CAMERA_SIOD)
print("construct camera")
cam = adafruit_ov5640.OV5640(
    bus,
    data_pins=board.CAMERA_DATA,
    clock=board.CAMERA_PCLK,
    vsync=board.CAMERA_VSYNC,
    href=board.CAMERA_HREF,
    mclk=board.CAMERA_XCLK,
    size=adafruit_ov5640.OV5640_SIZE_QQVGA,
)
print("print chip id")
print(cam.chip_id)


cam.colorspace = adafruit_ov5640.OV5640_COLOR_YUV
cam.flip_y = True
cam.flip_x = True
cam.test_pattern = False

buf = bytearray(cam.capture_buffer_size)
chars = b" .':-+=*%$#"
remap = [chars[i * (len(chars) - 1) // 255] for i in range(256)]

width = cam.width
row = bytearray(width)

print("capturing")
cam.capture(buf)
print("capture complete")

sys.stdout.write("\033[2J")
while True:
    cam.capture(buf)
    for j in range(0, cam.height, 2):
        sys.stdout.write(f"\033[{j//2}H")
        for i in range(cam.width):
            row[i] = remap[buf[2 * (width * j + i)]]
        sys.stdout.write(row)
        sys.stdout.write("\033[K")
    sys.stdout.write("\033[J")
    time.sleep(0.05)
