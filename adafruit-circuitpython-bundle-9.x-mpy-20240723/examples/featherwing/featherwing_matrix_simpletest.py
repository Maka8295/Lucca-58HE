# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example will demonstrate some graphic effects and then
draw a smiley face and shift it around the display
"""
import time
from adafruit_featherwing import matrix_featherwing

matrix = matrix_featherwing.MatrixFeatherWing()

# Create a Fade-in Effect
matrix.brightness = 0
matrix.fill(True)
for level in range(0, 16):
    matrix.brightness = level
    time.sleep(0.1)

# Show the different Blink Rates
for level in range(3, -1, -1):
    matrix.blink_rate = level
    time.sleep(4)

# Create a Fade-out Effect
for level in range(15, -1, -1):
    matrix.brightness = level
    time.sleep(0.1)
matrix.fill(False)

# Reset the brightness to full
matrix.brightness = 15

# Clear the Screen
matrix.fill(False)

# Draw a Smiley Face
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
        matrix.shift_right()
    for frame in range(0, 8):
        matrix.shift_down(True)
    for frame in range(0, 8):
        matrix.shift_left()
    for frame in range(0, 8):
        matrix.shift_up(True)
