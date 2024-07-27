# SPDX-FileCopyrightText: 2021 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Test the wrap_text_to_pixels function. Try changing WRAP_WIDTH or text
and observe the results. The red bar represents the full size of
WRAP_WIDTH.
"""

import board
import displayio
import terminalio
from adafruit_display_text import label, wrap_text_to_pixels

WRAP_WIDTH = 140
text = (
    "CircuitPython is a programming language designed to simplify experimenting "
    "and learning to code on low-cost microcontroller boards. "
)

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

# Make the display context
main_group = displayio.Group()
display.root_group = main_group

font = terminalio.FONT

print(text)
print(display.width)

text_area = label.Label(
    font,
    text="\n".join(wrap_text_to_pixels(text, WRAP_WIDTH, font)),
    background_color=0x0000DD,
)

text_area.anchor_point = (0, 0)
text_area.anchored_position = (0, 0)

main_group.append(text_area)

# Create a bitmap with two colors
size_checker = displayio.Bitmap(WRAP_WIDTH, 10, 2)
# Create a two color palette
palette = displayio.Palette(2)
palette[0] = 0x0000DD
palette[1] = 0xDD0000

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(size_checker, pixel_shader=palette)

tile_grid.y = text_area.bounding_box[1] + text_area.bounding_box[3] + 10

size_checker.fill(1)

main_group.append(tile_grid)

while True:
    pass
