# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example plays various animations
and then draws random pixels at random locations
"""

from time import sleep
import random
from adafruit_featherwing import neopixel_featherwing

neopixel = neopixel_featherwing.NeoPixelFeatherWing()

# HELPERS
# a random color 0 -> 224
def random_color():
    return random.randrange(0, 8) * 32


# Fill screen with random colors at random brightnesses
for i in range(0, 5):
    neopixel.fill((random_color(), random_color(), random_color()))
    neopixel.brightness = random.randrange(2, 10) / 10
    sleep(0.2)

# Set display to 30% brightness
neopixel.brightness = 0.3

# Create a gradiant drawing each pixel
for x in range(0, neopixel.columns):
    for y in range(neopixel.rows - 1, -1, -1):
        neopixel[x, y] = (y * 63, 255, y * 63)

# Rotate everything left 36 frames
for i in range(0, 36):
    neopixel.shift_down(True)
    sleep(0.1)

# Draw dual gradiant and then update
# neopixel.auto_write = False
for y in range(0, neopixel.rows):
    for x in range(0, 4):
        neopixel[x, y] = (y * 16 + 32, x * 8, 0)
    for x in range(4, 8):
        neopixel[x, y] = ((4 - y) * 16 + 32, (8 - x) * 8, 0)
neopixel.show()

# Rotate everything left 36 frames
for i in range(0, 36):
    neopixel.shift_left(True)
    neopixel.shift_up(True)
    neopixel.show()
    sleep(0.1)
neopixel.auto_write = True

# Shift pixels without rotating for an animated screen wipe
for i in range(0, neopixel.rows):
    neopixel.shift_down()
    sleep(0.4)

# Show pixels in random locations of random color
# Bottom left corner is (0,0)
while True:
    x = random.randrange(0, neopixel.columns)
    y = random.randrange(0, neopixel.rows)
    neopixel[x, y] = (random_color(), random_color(), random_color())
    sleep(0.1)
