# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import displayio
from adafruit_progressbar.verticalprogressbar import (
    VerticalProgressBar,
    VerticalFillDirection,
)

# Make the display context
splash = displayio.Group()
board.DISPLAY.root_group = splash

# set progress bar width and height relative to board's display
width = 10
height = board.DISPLAY.height - 40

x = width * 2
y = 10

# Create a new VerticalProgressBar object at (x, y)
vertical_progress_bar = VerticalProgressBar(
    (x, y), (width, height), direction=VerticalFillDirection.TOP_TO_BOTTOM
)

# Append progress_bar to the splash group
splash.append(vertical_progress_bar)

x = x * 2
# Create a second VerticalProgressBar object at (x+20, y)
vertical_progress_bar2 = VerticalProgressBar(
    (x, y), (width, height), direction=VerticalFillDirection.BOTTOM_TO_TOP
)

# Append progress_bar to the splash group
splash.append(vertical_progress_bar2)


current_progress = 0.0
while True:
    # range end is exclusive so we need to use 1 bigger than max number that we want
    for current_progress in range(0, 101, 1):
        print("Progress: {}%".format(current_progress))
        vertical_progress_bar.value = current_progress
        vertical_progress_bar2.value = current_progress
        time.sleep(0.05)
    time.sleep(0.3)
    vertical_progress_bar.value = vertical_progress_bar.minimum
    vertical_progress_bar2.value = vertical_progress_bar.minimum
    time.sleep(0.3)
