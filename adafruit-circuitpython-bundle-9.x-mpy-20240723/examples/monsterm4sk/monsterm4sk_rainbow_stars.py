# SPDX-FileCopyrightText: 2020 Foamyguy, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
CircuitPython example for Monster M4sk.

Draws star images on each screen. When buttons are pressed
set the stars to a different color. When the nose is booped
make the eyes change through the rainbow.
"""

import time
import board
import displayio
import adafruit_imageload
import adafruit_monsterm4sk


SCREEN_SIZE = 240
IMAGE_SIZE = 64 * 3

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

mask = adafruit_monsterm4sk.MonsterM4sk(i2c=i2c_bus)

left_group = displayio.Group(scale=3)
mask.left_display.root_group = left_group

right_group = displayio.Group(scale=3)
mask.right_display.root_group = right_group

left_group.x = (SCREEN_SIZE - IMAGE_SIZE) // 2
left_group.y = (SCREEN_SIZE - IMAGE_SIZE) // 2

right_group.x = (SCREEN_SIZE - IMAGE_SIZE) // 2
right_group.y = (SCREEN_SIZE - IMAGE_SIZE) // 2

#  load in party parrot bitmap
star_bitmap, star_palette = adafruit_imageload.load(
    "/rainbow_star.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
)

right_star_grid = displayio.TileGrid(
    star_bitmap,
    pixel_shader=star_palette,
    width=1,
    height=1,
    tile_height=64,
    tile_width=64,
    default_tile=0,
    x=0,
    y=0,
)

left_star_grid = displayio.TileGrid(
    star_bitmap,
    pixel_shader=star_palette,
    width=1,
    height=1,
    tile_height=64,
    tile_width=64,
    default_tile=0,
    x=0,
    y=0,
)

right_group.append(right_star_grid)
left_group.append(left_star_grid)
while True:
    if mask.boop:
        for i in range(6 * 3):
            right_star_grid[0] = i % 6
            left_star_grid[0] = i % 6
            time.sleep(0.02)
        time.sleep(0.5)

    if mask.buttons["S9"]:
        right_star_grid[0] = 2
        left_star_grid[0] = 2

    if mask.buttons["S10"]:
        right_star_grid[0] = 4
        left_star_grid[0] = 4

    if mask.buttons["S11"]:
        right_star_grid[0] = 3
        left_star_grid[0] = 3
