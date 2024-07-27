# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from random import randrange
import displayio
from adafruit_gizmo import tft_gizmo

# Create the TFT Gizmo display
display = tft_gizmo.TFT_Gizmo()

# You can now use the display to do whatever you want
# Here we show how to draw random pixels

# Create a bitmap with two colors
bitmap = displayio.Bitmap(display.width, display.height, 2)

# Create a two color palette
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xFFFFFF

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group

# Draw pixels
while True:
    for _ in range(200):
        x = randrange(0, display.width)
        y = randrange(0, display.height)
        bitmap[x, y] = 1
        time.sleep(0.1)
    for i in range(display.width * display.height):
        bitmap[i] = 0
