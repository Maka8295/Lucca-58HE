# SPDX-FileCopyrightText: 2022 Tim Cocks for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import displayio
import adafruit_imageload
from adafruit_imageload.tilegrid_inflator import inflate_tilegrid

image, palette = adafruit_imageload.load("images/castle_spritesheet.bmp")
tile_grid = inflate_tilegrid(bmp_obj=image, bmp_palette=palette, target_size=(10, 8))

group = displayio.Group()
group.append(tile_grid)
board.DISPLAY.root_group = group

while True:
    pass
