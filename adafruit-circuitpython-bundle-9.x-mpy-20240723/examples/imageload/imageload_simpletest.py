# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import displayio
import adafruit_imageload

image, palette = adafruit_imageload.load("images/4bit.bmp")

tile_grid = displayio.TileGrid(image, pixel_shader=palette)

group = displayio.Group()
group.append(tile_grid)
board.DISPLAY.root_group = group

while True:
    pass
