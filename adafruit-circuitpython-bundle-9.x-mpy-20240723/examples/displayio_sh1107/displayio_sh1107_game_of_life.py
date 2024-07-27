# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Author: Mark Roberts (mdroberts1243) from Adafruit code
Conway's game of life.
"""


import random
import time

import board
import displayio

# Compatibility with both CircuitPython 8.x.x and 9.x.x.
# Remove after 8.x.x is no longer a supported release.
try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

import adafruit_displayio_sh1107

displayio.release_displays()


def apply_life_rule(old, new):
    """
    Conway's "Game of Life" is played on a grid with simple rules, based
    on the number of filled neighbors each cell has and whether the cell itself
    is filled.
      * If the cell is filled, and 2 or 3 neighbors are filled, the cell stays
        filled
      * If the cell is empty, and exactly 3 neighbors are filled, a new cell
        becomes filled
      * Otherwise, the cell becomes or remains empty

    The complicated way that the "m1" (minus 1) and "p1" (plus one) offsets are
    calculated is due to the way the grid "wraps around", with the left and right
    sides being connected, as well as the top and bottom sides being connected.

    This function has been somewhat optimized, so that when it indexes the bitmap
    a single number [x + width * y] is used instead of indexing with [x, y].
    This makes the animation run faster with some loss of clarity. More
    optimizations are probably possible.
    """
    width = old.width
    height = old.height
    for y in range(height):
        yyy = y * width
        ym1 = ((y + height - 1) % height) * width
        yp1 = ((y + 1) % height) * width
        xm1 = width - 1
        for x in range(width):
            xp1 = (x + 1) % width
            neighbors = (
                old[xm1 + ym1]
                + old[xm1 + yyy]
                + old[xm1 + yp1]
                + old[x + ym1]
                + old[x + yp1]
                + old[xp1 + ym1]
                + old[xp1 + yyy]
                + old[xp1 + yp1]
            )
            new[x + yyy] = neighbors == 3 or (neighbors == 2 and old[x + yyy])
            xm1 = x


def randomize(output, fraction=0.33):
    """Fill 'fraction' out of all the cells."""
    for i in range(output.height * output.width):
        output[i] = random.random() < fraction


def conway(output):
    """
    Fill the grid with a tribute to John Conway.

    Based on xkcd's tribute to John Conway (1937-2020) https://xkcd.com/2293/
    """
    conway_data = [
        b"  +++   ",
        b"  + +   ",
        b"  + +   ",
        b"   +    ",
        b"+ +++   ",
        b" + + +  ",
        b"   +  + ",
        b"  + +   ",
        b"  + +   ",
    ]
    for i in range(output.height * output.width):
        output[i] = 0
    for i, si in enumerate(conway_data):
        y = output.height - len(conway_data) - 2 + i
        for j, cj in enumerate(si):
            output[(output.width - 8) // 2 + j, y] = cj & 1


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = I2CDisplayBus(i2c, device_address=0x3C)

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

SCALE = 2  # scale up for the small OLED pixels!

b1 = displayio.Bitmap(display.width // SCALE, display.height // SCALE, 2)
b2 = displayio.Bitmap(display.width // SCALE, display.height // SCALE, 2)
palette = displayio.Palette(2)
tg1 = displayio.TileGrid(b1, pixel_shader=palette)
tg2 = displayio.TileGrid(b2, pixel_shader=palette)
g1 = displayio.Group(scale=SCALE)
g1.append(tg1)
display.root_group = g1
g2 = displayio.Group(scale=SCALE)
g2.append(tg2)

# First time, show the Conway tribute
palette[1] = 0xFFFFFF
conway(b1)
display.auto_refresh = True
time.sleep(3)
n = 40

while True:
    # run 2*n generations.
    # For the Conway tribute on 64x32, 80 frames is appropriate.  For random
    # values, 400 frames seems like a good number.  Working in this way, with
    # two bitmaps, reduces copying data and makes the animation a bit faster
    for _ in range(n):
        display.root_group = g1
        apply_life_rule(b1, b2)
        display.root_group = g2
        apply_life_rule(b2, b1)

    # After 2*n generations, fill the board with random values and
    # start over with a new color.
    randomize(b1)
    # Only white for the OLED display
    palette[1] = 0xFFFFFF
    n = 100
