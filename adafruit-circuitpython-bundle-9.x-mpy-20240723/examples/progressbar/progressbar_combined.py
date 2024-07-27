#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Hugo Dahl for Adafruit Industries
# SPDX-License-Identifier: MIT

# Before you can run this example, you will need to install the
# required libraries identifies in the `requirements.txt` file.
# You can do so automatically by using the "pip" utility.

import time
import board
import displayio
from adafruit_progressbar.horizontalprogressbar import HorizontalProgressBar
from adafruit_progressbar.verticalprogressbar import VerticalProgressBar

# Make the display context
splash = displayio.Group()
board.DISPLAY.root_group = splash

# set horizontal progress bar width and height relative to board's display
h_width = board.DISPLAY.width - 40
h_height = 30

v_width = 30
v_height = 140

h_x = 20
h_y = 20

v_x = 60
v_y = 70

# Create a new progress_bar objects at their x, y locations
progress_bar = HorizontalProgressBar((h_x, h_y), (h_width, h_height), 0, 100)
vert_progress_bar = VerticalProgressBar((v_x, v_y), (v_width, v_height), 0, 200)

# Append progress_bars to the splash group
splash.append(progress_bar)
splash.append(vert_progress_bar)

current_progress = 0.0
while True:
    # range end is exclusive so we need to use 1 bigger than max number that we want
    for current_progress in range(0, 101, 1):
        print("Progress: {}%".format(current_progress))
        progress_bar.value = current_progress
        vert_progress_bar.value = current_progress * 2
        time.sleep(0.01)
    time.sleep(0.3)
    # reset to empty
    progress_bar.value = 0
    vert_progress_bar.value = 0
    time.sleep(0.3)
