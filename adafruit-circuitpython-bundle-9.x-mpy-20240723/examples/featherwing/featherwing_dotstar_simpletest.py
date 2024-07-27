# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This plays various animations
and then draws random pixels at random locations
"""

from time import sleep
import random
from adafruit_featherwing import dotstar_featherwing

dotstar = dotstar_featherwing.DotStarFeatherWing()

# HELPERS
# a random color 0 -> 224
def random_color():
    return random.randrange(0, 8) * 32


# Fill screen with random colors at random brightnesses
for i in range(0, 5):
    dotstar.fill((random_color(), random_color(), random_color()))
    dotstar.brightness = random.randrange(2, 10) / 10
    sleep(0.2)

# Set display to 30% brightness
dotstar.brightness = 0.3

# Create a gradiant drawing each pixel
for x in range(0, dotstar.columns):
    for y in range(dotstar.rows - 1, -1, -1):
        dotstar[x, y] = (y * 42, 255, y * 42, 1)

# Rotate everything left 36 frames
for i in range(0, 36):
    dotstar.shift_down(True)

# Draw dual gradiant and then update
dotstar.auto_write = False
for y in range(0, dotstar.rows):
    for x in range(0, 6):
        dotstar[x, y] = (y * 84, x * 42, x * 42, 1)
    for x in range(6, 12):
        dotstar[x, y] = (255 - (y * 84), 255 - ((x - 6) * 42), 255 - ((x - 6) * 42), 1)

# Rotate everything left 36 frames
for i in range(0, 36):
    dotstar.shift_left(True)
    dotstar.shift_up(True)
    dotstar.show()
dotstar.auto_write = True

# Shift pixels without rotating for an animated screen wipe
for i in range(0, 6):
    dotstar.shift_down()

# Show pixels in random locations of random color
# Bottom left corner is (0,0)
while True:
    x = random.randrange(0, dotstar.columns)
    y = random.randrange(0, dotstar.rows)
    dotstar[x, y] = (random_color(), random_color(), random_color())
    sleep(0.1)
