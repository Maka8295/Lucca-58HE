# SPDX-FileCopyrightText: 2022 Tim Cocks
# SPDX-License-Identifier: MIT

import board
import displayio
from vectorio import Rectangle
import adafruit_imageload

# built-in display
display = board.DISPLAY

# load png image
image, palette = adafruit_imageload.load("images/test_image.png")

# Set the transparency index color to be hidden
palette.make_transparent(0)

# make tilegrid for the loaded image
tile_grid = displayio.TileGrid(image, pixel_shader=palette)
tile_grid.x = display.width // 2 - tile_grid.tile_width // 2
tile_grid.y = display.height // 2 - tile_grid.tile_height // 2

# make a blank background
bg_palette = displayio.Palette(1)
bg_palette[0] = 0xFFFFFF
rect = Rectangle(
    pixel_shader=bg_palette, width=display.width, height=display.height, x=0, y=0
)

# make a group to show on the display
group = displayio.Group()

# add background
group.append(rect)
# add loaded image tilegrid
group.append(tile_grid)

# show our group
board.DISPLAY.root_group = group

# loop forever so it stays on the display
while True:
    pass
