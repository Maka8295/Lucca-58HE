# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example of drawing an image
# This example and library is meant to work with Adafruit CircuitPython API.
#
# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
#
# Author: Melissa LeBlanc-Williams
# License: Public Domain

# Import all board pins.
import board
import busio
from PIL import Image

# Import the HT16K33 LED matrix module.
from adafruit_ht16k33 import matrix

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the matrix class.
# This creates a 16x8 matrix:
mtrx = matrix.Matrix16x8(i2c)
# Or this creates a 16x8 matrix backpack:
# mtrx = matrix.MatrixBackpack16x8(i2c)
# Or this creates a 8x8 matrix:
# mtrx = matrix.Matrix8x8(i2c)
# Or this creates a 8x8 bicolor matrix:
# mtrx = matrix.Matrix8x8x2(i2c)
# Finally you can optionally specify a custom I2C address of the HT16k33 like:
# mtrx = matrix.Matrix16x8(i2c, address=0x70)

if isinstance(mtrx, matrix.Matrix8x8x2):
    image = Image.open("squares-color.png")
elif isinstance(mtrx, matrix.Matrix16x8):
    image = Image.open("squares-mono-16x8.png")
else:
    image = Image.open("squares-mono-8x8.png")

# Clear the matrix
mtrx.fill(0)
mtrx.image(image)
