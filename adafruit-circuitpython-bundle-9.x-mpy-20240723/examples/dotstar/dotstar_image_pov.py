# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

#!/usr/bin/python3

# Persistence-of-vision (POV) example for Adafruit DotStar RGB LED strip.
# Loads image, displays column-at-a-time on LEDs at very high speed,
# suitable for naked-eye illusions.
# See dotstar_simpletest.py for a much simpler example script.
# See dotstar_image_paint.py for a slightly simpler light painting example.
# This code accesses some elements of the dotstar object directly rather
# than through function calls or setters/getters...this is poor form as it
# could break easily with future library changes, but is the only way right
# now to do the POV as quickly as possible.
# May require installing separate libraries.

import board
from PIL import Image
import adafruit_dotstar as dotstar

NUMPIXELS = 30  # Length of DotStar strip
FILENAME = "hello.png"  # Image file to load
ORDER = dotstar.BGR  # Change to GBR for older DotStar strips

# First two arguments in strip declaration identify the clock and data pins
# (here we're using the hardware SPI pins).
DOTS = dotstar.DotStar(
    board.SCK,
    board.MOSI,
    NUMPIXELS,
    auto_write=False,
    brightness=1.0,
    pixel_order=ORDER,
)

# Load image in RGB format and get dimensions:
print("Loading...")
IMG = Image.open(FILENAME).convert("RGB")
PIXELS = IMG.load()
WIDTH = IMG.size[0]
HEIGHT = IMG.size[1]
print("%dx%d pixels" % IMG.size)

HEIGHT = min(HEIGHT, NUMPIXELS)

# Calculate gamma correction table, makes mid-range colors look 'right':
GAMMA = bytearray(256)
brightness = 0.25
for i in range(256):
    GAMMA[i] = int(pow(float(i) / 255.0, 2.7) * brightness * 255.0 + 0.5)

# Allocate list of lists, one for each column of image.
print("Allocating...")
COLUMN = [0 for x in range(WIDTH)]
for x in range(WIDTH):
    COLUMN[x] = [[0, 0, 0, 0] for _ in range(HEIGHT)]

# Convert entire RGB image into columnxrow 2D list.
print("Converting...")
for x in range(WIDTH):  # For each column of image
    for y in range(HEIGHT):  # For each pixel in column
        value = PIXELS[x, y]  # Read RGB pixel in image
        COLUMN[x][y][0] = GAMMA[value[0]]  # Gamma-corrected R
        COLUMN[x][y][1] = GAMMA[value[1]]  # Gamma-corrected G
        COLUMN[x][y][2] = GAMMA[value[2]]  # Gamma-corrected B
        COLUMN[x][y][3] = 1.0  # Brightness

print("Displaying...")
while True:  # Loop forever
    for x in range(WIDTH):  # For each column of image...
        DOTS[0 : DOTS.n] = COLUMN[x]  # Copy column to DotStar buffer
        DOTS.show()  # Send data to strip
