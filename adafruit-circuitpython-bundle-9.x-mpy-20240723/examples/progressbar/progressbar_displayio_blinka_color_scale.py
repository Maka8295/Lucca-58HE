#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Hugo Dahl for Adafruit Industries
# SPDX-FileCopyrightText: 2021 Jose David M.
# SPDX-License-Identifier: MIT

# Before you can run this example, you will need to install the
# required libraries identifies in the `requirements.txt` file.
# You can do so automatically by using the "pip" utility.

"""
Shows the ability of the progress bar to change color on the fly.
This example is and adaptation from the progressbar_displayio_blinka test
"""

import time
import adafruit_fancyled.adafruit_fancyled as fancy
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)

display = PyGameDisplay(width=320, height=240, auto_refresh=False)
splash = displayio.Group()
display.root_group = splash

# Setting up the grayscale values, You could use a different scale, and add more entries
# to have detailed transitions
# see learning guide regarding the FancyLed library
# https://learn.adafruit.com/fancyled-library-for-circuitpython/palettes
grad = [
    (0.0, 0x000000),
    (0.20, 0x333333),
    (0.40, 0x666666),
    (0.60, 0x999999),
    (0.80, 0xCCCCCC),
    (1.0, 0xEEEEEE),
]

# Creating the grayscale Palette using the FancyLed Library
palette = fancy.expand_gradient(grad, 50)

colors = []

# We create an equal space palette. This is done for convenience and clarity as we use
# a value from 0 to 100 in our ProgressBar
for i in range(99):
    color = fancy.palette_lookup(palette, i / 100)
    colors.append(color.pack())

# Background creation
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x2266AA  # Teal-ish-kinda

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)


horizontal_bar = HorizontalProgressBar(
    (10, 80),
    (180, 40),
    fill_color=0x990099,
    outline_color=0x0000FF,
    bar_color=0x00FF00,
    direction=HorizontalFillDirection.LEFT_TO_RIGHT,
)
splash.append(horizontal_bar)

# List of step values for the progress bar
test_value_range_1 = list(range(99))

# Must check display.running in the main loop!
while display.running:
    print("\nDemonstration of values between 0 and 100 - Horizontal")
    for val in test_value_range_1:
        horizontal_bar.value = val
        horizontal_bar.bar_color = colors[val]
        display.refresh()
        time.sleep(0.1)
