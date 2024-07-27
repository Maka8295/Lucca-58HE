# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Source: https://github.com/ajs256/matrixportal-weather-display

# ############## IMPORTS ###############

# HARDWARE
import time
import board

# DISPLAY
import displayio  # Main display library
import framebufferio  # For showing things on the display
import rgbmatrix  # For talking to matrices specifically

# CONTROLS

import digitalio

from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)
from adafruit_progressbar.verticalprogressbar import (
    VerticalProgressBar,
    VerticalFillDirection,
)

# ############## DISPLAY SETUP ###############

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()

print("Setting up RGB matrix")

# This next call creates the RGB Matrix object itself. It has the given width
# and height.
#
# These lines are for the Matrix Portal. If you're using a different board,
# check the guide to find the pins and wiring diagrams for your board.
# If you have a matrix with a different width or height, change that too.
matrix = rgbmatrix.RGBMatrix(
    width=64,
    height=32,
    bit_depth=3,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2,
    ],
    addr_pins=[board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE,
)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix)

print("Adding display group")
group = displayio.Group()  # Create a group to hold all our labels
display.root_group = group

print("Creating progress bars and adding to group")

# A horizontal percentage progress bar, valued at 60%
progress_bar = HorizontalProgressBar((2, 8), (40, 8), value=60)
group.insert(0, progress_bar)

# Another progress bar, with explicit range and fill from the right
ranged_bar = HorizontalProgressBar(
    (2, 20),
    (40, 8),
    value=40,
    min_value=0,
    max_value=100,
    direction=HorizontalFillDirection.RIGHT_TO_LEFT,
)
group.insert(1, ranged_bar)

# Sample thermometer from -40C to 50C, with a value of +15C
vertical_bar = VerticalProgressBar(
    (44, 4),
    (8, 24),
    min_value=-40,
    max_value=50,
    value=15,
    bar_color=0x1111FF,
    fill_color=None,
    margin_size=0,
    outline_color=0x2222AA,
)
group.insert(2, vertical_bar)

vertical_bar2 = VerticalProgressBar(
    (54, 4),
    (8, 24),
    min_value=-40,
    max_value=50,
    value=15,
    bar_color=0x1111FF,
    fill_color=None,
    margin_size=0,
    outline_color=0x2222AA,
    direction=VerticalFillDirection.TOP_TO_BOTTOM,
)
group.insert(3, vertical_bar2)

# Countdown to the start of the bars demo
countdown_bar = HorizontalProgressBar(
    (2, 2),
    (20, 5),
    0,
    5,
    value=5,
    bar_color=0x11FF11,
    fill_color=0x333333,
    border_thickness=0,
    margin_size=0,
)

countdown_end_color = 0xFF1111

group.insert(4, countdown_bar)
# group.insert(0, countdown_bar)

print("Progress bars added. Starting demo...")

print("Using countdown bar")

for timer in range(countdown_bar.maximum, countdown_bar.minimum, -1):
    bar_color_to_set = (0x20 * (6 - timer) + 20, (0x20 * (timer - 1)) + 20, 0x10)
    countdown_bar.bar_color = bar_color_to_set
    countdown_bar.value = timer
    time.sleep(1)

print("Removing countdown bar")

countdown_bar.value = 0
group.remove(countdown_bar)

progress_bar_value = 0.0
progress_bar_incr = 3.0

button1 = digitalio.DigitalInOut(board.BUTTON_UP)
button1.switch_to_input(digitalio.Pull.UP)
button2 = digitalio.DigitalInOut(board.BUTTON_DOWN)
button2.switch_to_input(digitalio.Pull.UP)


print("Start forever loop")
while True:
    print("Setting progress bar value to", progress_bar_value)

    progress_bar.value = progress_bar_value
    ranged_bar.value = progress_bar_value
    progress_bar_value += progress_bar_incr

    if not (button1.value and button2.value):
        if not button1.value:  # "UP" button pushed
            print("UP button pressed. Increasing vertical bars by 3")
            vertical_bar.value = min(vertical_bar.maximum, vertical_bar.value + 3)
            vertical_bar2.value = min(vertical_bar2.maximum, vertical_bar2.value + 3)

        if not button2.value:  # "DOWN" button pushed
            print("DOWN button pressed. Decreasing vertical bars by 3")
            vertical_bar.value = max(vertical_bar.minimum, vertical_bar.value - 3)
            vertical_bar2.value = max(vertical_bar2.minimum, vertical_bar2.value - 3)

    if progress_bar_value > progress_bar.maximum:
        progress_bar_value = progress_bar.maximum
        progress_bar_incr *= -1

    if progress_bar_value < progress_bar.minimum:
        progress_bar_value = progress_bar.minimum
        progress_bar_incr *= -1

    time.sleep(0.5)
