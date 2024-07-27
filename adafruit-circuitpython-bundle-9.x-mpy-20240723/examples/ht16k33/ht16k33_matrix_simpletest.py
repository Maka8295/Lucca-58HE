# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example of clearing and drawing a pixel on a LED matrix display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

# Import all board pins.
import time
import board
import busio

# Import the HT16K33 LED matrix module.
from adafruit_ht16k33 import matrix


# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the matrix class.
# This creates a 16x8 matrix:
matrix = matrix.Matrix16x8(i2c)
# Or this creates a 16x8 matrix backpack:
# matrix = matrix.MatrixBackpack16x8(i2c)
# Or this creates a 8x8 matrix:
# matrix = matrix.Matrix8x8(i2c)
# Or this creates a 8x8 bicolor matrix:
# matrix = matrix.Matrix8x8x2(i2c)
# Finally you can optionally specify a custom I2C address of the HT16k33 like:
# matrix = matrix.Matrix16x8(i2c, address=0x70)

# Clear the matrix.
matrix.fill(0)

# Set a pixel in the origin 0, 0 position.
matrix[0, 0] = 1
# Set a pixel in the middle 8, 4 position.
matrix[8, 4] = 1
# Set a pixel in the opposite 15, 7 position.
matrix[15, 7] = 1

time.sleep(2)

# Draw a Smiley Face
matrix.fill(0)

for row in range(2, 6):
    matrix[row, 0] = 1
    matrix[row, 7] = 1

for column in range(2, 6):
    matrix[0, column] = 1
    matrix[7, column] = 1

matrix[1, 1] = 1
matrix[1, 6] = 1
matrix[6, 1] = 1
matrix[6, 6] = 1
matrix[2, 5] = 1
matrix[5, 5] = 1
matrix[2, 3] = 1
matrix[5, 3] = 1
matrix[3, 2] = 1
matrix[4, 2] = 1

# Move the Smiley Face Around
while True:
    for frame in range(0, 8):
        matrix.shift_right(True)
        time.sleep(0.05)
    for frame in range(0, 8):
        matrix.shift_down(True)
        time.sleep(0.05)
    for frame in range(0, 8):
        matrix.shift_left(True)
        time.sleep(0.05)
    for frame in range(0, 8):
        matrix.shift_up(True)
        time.sleep(0.05)
