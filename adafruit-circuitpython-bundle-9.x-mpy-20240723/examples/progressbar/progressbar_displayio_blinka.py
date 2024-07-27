#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Hugo Dahl for Adafruit Industries
# SPDX-License-Identifier: MIT

# Before you can run this example, you will need to install the
# required libraries identifies in the `requirements.txt` file.
# You can do so automatically by using the "pip" utility.

import time
import sys
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_progressbar.progressbar import ProgressBar
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)
from adafruit_progressbar.verticalprogressbar import (
    VerticalProgressBar,
    VerticalFillDirection,
)

display = PyGameDisplay(width=320, height=240, auto_refresh=False)
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x2266AA  # Teal-ish-kinda

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

progress_bar = ProgressBar(
    width=180,
    height=40,
    x=10,
    y=20,
    progress=0.0,
    bar_color=0x1100FF,
    outline_color=0x777777,
)
splash.append(progress_bar)

horizontal_bar = HorizontalProgressBar(
    (10, 80),
    (180, 40),
    fill_color=0x778822,
    outline_color=0x0000FF,
    bar_color=0x00FF00,
    direction=HorizontalFillDirection.LEFT_TO_RIGHT,
)
splash.append(horizontal_bar)

horizontal_thermometer = HorizontalProgressBar(
    (10, 140),
    (180, 40),
    value=-10,
    min_value=(-40),
    max_value=130,
    fill_color=0x00FF00,
    outline_color=0x0000FF,
    bar_color=0x22BB88,
    direction=HorizontalFillDirection.RIGHT_TO_LEFT,
)
splash.append(horizontal_thermometer)

vertical_bar = VerticalProgressBar(
    (200, 30),
    (32, 180),
    direction=VerticalFillDirection.TOP_TO_BOTTOM,
)
splash.append(vertical_bar)

vertical_thermometer = VerticalProgressBar(
    (260, 30),
    (32, 180),
    min_value=-40,
    max_value=130,
    direction=VerticalFillDirection.BOTTOM_TO_TOP,
)
splash.append(vertical_thermometer)

test_value_range_1 = [99, 100, 99, 1, 0, 1]
test_value_range_2 = [120, 130, 129, -20, -39, -40, -28]
delay = 2
_incr = 1

# Must check display.running in the main loop!
while display.running:
    print("\nDemonstration of legacy functionality and syntax, increment by 0.01")
    for val in range(0, 101):
        if not display.running:
            sys.exit(0)
        _use_value = round((val * 0.01), 2)
        if (val % 10) == 0:
            print(f"Value has reached {_use_value:2}")
        progress_bar.progress = round(_use_value, 2)
        display.refresh()
        time.sleep(0.05)

    print("\nDemonstration of values between 0 and 100 - Horizontal and vertical")
    for val in test_value_range_1:
        if not display.running:
            sys.exit(0)
        print(f"Setting value to {val}")
        vertical_bar.value = val
        horizontal_bar.value = val
        display.refresh()
        time.sleep(delay)

    print("\nDemonstration of Fahrenheit range -40 and 130 - Horizontal and vertical")
    for val in test_value_range_2:
        if not display.running:
            sys.exit(0)
        print(f"Setting value to {val}")
        vertical_thermometer.value = val
        horizontal_thermometer.value = val
        display.refresh()
        time.sleep(delay)
