# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import displayio
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)

# Make the display context
splash = displayio.Group()
board.DISPLAY.root_group = splash

# set progress bar width and height relative to board's display
width = board.DISPLAY.width - 40
height = 30

x = board.DISPLAY.width // 2 - width // 2
y = board.DISPLAY.height // 3

# Create a new progress_bar object at (x, y)
progress_bar = HorizontalProgressBar(
    (x, y), (width, height), direction=HorizontalFillDirection.LEFT_TO_RIGHT
)

# Append progress_bar to the splash group
splash.append(progress_bar)

current_value = progress_bar.minimum
while True:
    # range end is exclusive so we need to use 1 bigger than max number that we want
    for current_value in range(progress_bar.minimum, progress_bar.maximum + 1, 1):
        print("Progress: {}%".format(current_value))
        progress_bar.value = current_value
        time.sleep(0.01)
    time.sleep(0.3)
    progress_bar.value = progress_bar.minimum
    time.sleep(0.3)
