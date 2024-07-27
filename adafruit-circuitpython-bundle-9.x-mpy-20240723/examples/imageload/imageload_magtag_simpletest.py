# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Basic imageload example script
adapted for use on MagTag.
"""
import time
import board
import displayio
import adafruit_imageload

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

# wait until the display is ready
time.sleep(display.time_to_refresh)

image, palette = adafruit_imageload.load("images/magtag_2x2_test.bmp")

tile_grid = displayio.TileGrid(image, pixel_shader=palette)

# scale 8 for full screen
group = displayio.Group(scale=8)
group.append(tile_grid)

# show the group and refresh
display.root_group = group
display.refresh()

while True:
    pass
