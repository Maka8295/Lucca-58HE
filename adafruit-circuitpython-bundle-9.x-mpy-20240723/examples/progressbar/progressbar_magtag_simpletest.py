# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Basic progressbar example script
adapted for use on MagTag.
"""
import time
import board
import displayio
import digitalio
from adafruit_progressbar.progressbar import HorizontalProgressBar

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY
time.sleep(display.time_to_refresh)

# B/up button will be used to increase the progress
up_btn = digitalio.DigitalInOut(board.BUTTON_B)
up_btn.direction = digitalio.Direction.INPUT
up_btn.pull = digitalio.Pull.UP

# C/down button will be used to increase the progress
down_btn = digitalio.DigitalInOut(board.BUTTON_C)
down_btn.direction = digitalio.Direction.INPUT
down_btn.pull = digitalio.Pull.UP

# Make the display context
splash = displayio.Group()
display.root_group = splash

# set progress bar width and height relative to board's display
BAR_WIDTH = display.width - 40
BAR_HEIGHT = 30

x = display.width // 2 - BAR_WIDTH // 2
y = display.height // 3

# Create a new progress_bar object at (x, y)
progress_bar = HorizontalProgressBar(
    (x, y),
    (BAR_WIDTH, BAR_HEIGHT),
    bar_color=0xFFFFFF,
    outline_color=0xAAAAAA,
    fill_color=0x777777,
)

# Append progress_bar to the splash group
splash.append(progress_bar)

# Get a random starting value within our min/max range
current_progress = time.monotonic() % 101
print(current_progress)
progress_bar.value = current_progress

# refresh the display
display.refresh()

value_incrementor = 3

prev_up = up_btn.value
prev_down = down_btn.value
while True:
    cur_up = up_btn.value
    cur_down = down_btn.value
    do_refresh = False
    # if up_btn was just pressed down
    if not cur_up and prev_up:
        current_progress += value_incrementor
        # Wrap if we get over the maximum value
        if current_progress > progress_bar.maximum:
            current_progress = progress_bar.minimum

        do_refresh = True

    if not cur_down and prev_down:
        current_progress -= value_incrementor
        # Wrap if we get below the minimum value
        if current_progress < progress_bar.minimum:
            current_progress = progress_bar.maximum

        do_refresh = True

    if do_refresh:
        print(current_progress)
        progress_bar.value = current_progress

        time.sleep(display.time_to_refresh)
        display.refresh()
        time.sleep(display.time_to_refresh)

    prev_up = cur_up
    prev_down = cur_down
