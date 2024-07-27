# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example of using FrameBuffer to create and scroll text on the matrix.

# Requires: adafruit_framebuf

import board
import busio
import adafruit_framebuf

# Import the HT16K33 LED matrix module.
from adafruit_ht16k33 import matrix

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the matrix class.
# This creates a 16x8 matrix:
matrix = matrix.Matrix16x8(i2c)

# Low brightness so it's easier to look at
matrix.brightness = 0

# Clear the matrix.
matrix.fill(0)

text_to_show = "Hello Blinka"

# Create a framebuffer for our display
buf = bytearray(16)  # 1 bytes tall x 16 wide = 16 bytes
fb = adafruit_framebuf.FrameBuffer(buf, 16, 8, adafruit_framebuf.MVLSB)


while True:
    for i in range(len(text_to_show) * 8):
        fb.fill(0)
        fb.text(text_to_show, -i + 16, 0, color=1)
        # turn all LEDs off
        matrix.fill(0)
        for x in range(16):
            # using the FrameBuffer text result
            bite = buf[x]
            for y in range(8):
                bit = 1 << y & bite
                # if bit > 0 then set the pixel brightness
                if bit:
                    matrix[16 - x, y + 1] = 1
