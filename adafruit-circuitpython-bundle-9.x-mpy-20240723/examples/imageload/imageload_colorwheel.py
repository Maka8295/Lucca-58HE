# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import displayio
import adafruit_imageload

display = board.DISPLAY

bitmap, palette = adafruit_imageload.load(
    "images/color_wheel.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
)

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

group = displayio.Group()
group.append(tile_grid)
display.root_group = group
while True:
    pass
