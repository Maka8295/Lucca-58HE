# SPDX-FileCopyrightText: 2021 Kevin Matocha
#
# SPDX-License-Identifier: MIT
"""
Creates multiple sliding switch widgets of various size and orientations.
"""

import time
import board
import displayio
import adafruit_touchscreen
from adafruit_displayio_layout.widgets.switch_round import SwitchRound as Switch

display = board.DISPLAY

# setup the touch screen
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(display.width, display.height),
)


# Create the switches

my_switch = Switch(20, 30)

my_switch2 = Switch(
    x=120,
    y=35,
    height=30,  # Set height to 30 pixels.  If you do not specify width,
    # it is automatically set to a default aspect ratio
    touch_padding=10,  # add extra boundary for touch response
    value=True,
)  # initial value is set to True

my_switch3 = Switch(
    x=20,
    y=85,
    height=40,
    fill_color_off=(255, 0, 0),  # Set off colorred, can use hex code (0xFF0000)
    outline_color_off=(80, 0, 0),
    background_color_off=(150, 0, 0),
    background_outline_color_off=(30, 0, 0),
)

my_switch4 = Switch(
    x=120,
    y=85,
    height=40,
    width=110,  # you can set the width manually but it may look weird
)

my_switch5 = Switch(
    x=20,
    y=140,
    height=40,
    display_button_text=False,  # do not show the 0/1 on the switch
)

my_switch6 = Switch(
    x=120,
    y=140,
    height=40,
    horizontal=False,  # set orientation to vertical
)

my_switch7 = Switch(
    x=180,
    y=140,
    height=40,
    horizontal=False,  # set orientation to vertical
    flip=True,  # swap the direction
)

my_switch8 = Switch(
    x=0,
    y=0,  # this is a larger, vertical orientation switch
    height=60,
    horizontal=False,  # set orientation to vertical
    flip=True,  # swap the direction
)
# use anchor_point and anchored_position to set the my_switch8 position
# relative to the display size.
my_switch8.anchor_point = (1.0, 1.0)
# the switch anchor_point is the bottom right switch corner
my_switch8.anchored_position = (display.width - 10, display.height - 10)
# the switch anchored_position is 10 pixels from the display
# lower right corner

my_group = displayio.Group()
my_group.append(my_switch)
my_group.append(my_switch2)
my_group.append(my_switch3)
my_group.append(my_switch4)
my_group.append(my_switch5)
my_group.append(my_switch6)
my_group.append(my_switch7)
my_group.append(my_switch8)

# Add my_group to the display
display.root_group = my_group


# Start the main loop
while True:
    p = ts.touch_point  # get any touches on the screen

    if p:  # Check each switch if the touch point is within the switch touch area
        # If touched, then flip the switch with .selected
        if my_switch.contains(p):
            my_switch.selected(p)

        elif my_switch2.contains(p):
            my_switch2.selected(p)

        elif my_switch3.contains(p):
            my_switch3.selected(p)

        elif my_switch4.contains(p):
            my_switch4.selected(p)

        elif my_switch5.contains(p):
            my_switch5.selected(p)

        elif my_switch6.contains(p):
            my_switch6.selected(p)

        elif my_switch7.contains(p):
            my_switch7.selected(p)

        elif my_switch8.contains(p):
            my_switch8.selected(p)

    time.sleep(0.05)  # touch response on PyPortal is more accurate with a small delay
