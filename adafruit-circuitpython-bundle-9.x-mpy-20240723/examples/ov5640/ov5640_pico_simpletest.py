# SPDX-FileCopyrightText: Copyright (c) 2023 Lady Ada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Capture an image from the camera and display it as ASCII art.

This demo is designed to run on the Raspberry Pi Pico, but you can adapt it
to other boards by changing the constructors for `bus` and `cam`
appropriately.

The camera is placed in YUV mode, so the top 8 bits of each color
value can be treated as "greyscale".

It's important that you use a terminal program that can interpret
"ANSI" escape sequences.  The demo uses them to "paint" each frame
on top of the previous one, rather than scrolling.

Remember to take the lens cap off!
"""
import sys
import time
import busio
import board
import digitalio
import adafruit_ov5640

print("construct bus")
bus = busio.I2C(board.GP9, board.GP8)
print("construct camera")
reset = digitalio.DigitalInOut(board.GP10)
cam = adafruit_ov5640.OV5640(
    bus,
    data_pins=(
        board.GP12,
        board.GP13,
        board.GP14,
        board.GP15,
        board.GP16,
        board.GP17,
        board.GP18,
        board.GP19,
    ),  # [16]     [org]
    clock=board.GP11,  # [15]     [blk]
    vsync=board.GP7,  # [10]     [brn]
    href=board.GP21,  # [27/o14] [red]
    mclk=board.GP20,  # [16/o15]
    shutdown=None,
    reset=reset,
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
    time.sleep(0.1)
