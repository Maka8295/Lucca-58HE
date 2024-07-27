# SPDX-FileCopyrightText: 2021 Kevin Matocha
#
# SPDX-License-Identifier: MIT
"""
Creates a single sliding switch widget.
"""

import time
import board
import displayio
import adafruit_touchscreen
from adafruit_displayio_layout.widgets.switch_round import SwitchRound as Switch

display = board.DISPLAY

ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(display.width, display.height),
)

# Create the switch
my_switch = Switch(20, 30)


my_group = displayio.Group()
my_group.append(my_switch)

# Add my_group to the display
display.root_group = my_group

# Start the main loop
while True:
    p = ts.touch_point  # get any touches on the screen

    if p:  # Check each switch if the touch point is within the switch touch area
        # If touched, then flip the switch with .selected
        if my_switch.contains(p):
            my_switch.selected(p)

    time.sleep(0.05)  # touch response on PyPortal is more accurate with a small delay
