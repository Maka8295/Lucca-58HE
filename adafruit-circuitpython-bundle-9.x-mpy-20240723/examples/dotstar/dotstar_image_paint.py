# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

#!/usr/bin/python3

# Light-painting example for Adafruit DotStar RGB LED strip.
# Loads image, displays column-at-a-time on LEDs at a reasonable
# speed for long exposure photography.
# See dotstar_simpletest.py for a much simpler example script.
# See dotstar_image_pov.py for a faster persistence-of-vision example.

import time
import board
from PIL import Image
import adafruit_dotstar as dotstar

NUMPIXELS = 30  # Number of LEDs in strip
FILENAME = "hello.png"  # Image file to load

# First two arguments in strip declaration identify the clock and data pins
# (here we're using the hardware SPI pins). Last argument identifies the
# color order -- older DotStar strips use GBR instead of BRG.
DOTS = dotstar.DotStar(
    board.SCK,
    board.MOSI,
    NUMPIXELS,
    brightness=0.25,
    auto_write=False,
    pixel_order=dotstar.BGR,
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
for i in range(256):
    GAMMA[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)

print("Displaying...")
while True:  # Loop forever
    for x in range(WIDTH):  # For each column of image...
        for y in range(HEIGHT):  # For each pixel in column...
            value = PIXELS[x, y]  # Read pixel in image
            DOTS[y] = (  # Set pixel #y in strip
                GAMMA[value[0]],  # Gamma-corrected red
                GAMMA[value[1]],  # Gamma-corrected green
                GAMMA[value[2]],  # Gamma-corrected blue
            )
        DOTS.show()  # Refresh LED strip
        time.sleep(0.01)  # Pause 1/100 sec.

    DOTS.fill(0)  # Clear strip and pause 1/4 sec.
    DOTS.show()
    time.sleep(0.25)
