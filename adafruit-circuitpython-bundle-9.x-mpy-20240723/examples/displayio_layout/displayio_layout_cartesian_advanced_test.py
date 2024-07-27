# SPDX-FileCopyrightText: 2021 Jose David M.
#
# SPDX-License-Identifier: MIT
#############################
"""
This is a more advance demonstration of a Cartesian widget and some configurable
parameters.
"""

import board
import displayio
import terminalio
from adafruit_displayio_layout.widgets.cartesian import Cartesian

# Fonts used for the Dial tick labels
tick_font = terminalio.FONT

display = board.DISPLAY  # create the display on the PyPortal or Clue (for example)
# otherwise change this to setup the display
# for display chip driver and pinout you have (e.g. ILI9341)


# Create different Cartesian widgets
my_group = displayio.Group()

car = Cartesian(
    x=25,
    y=10,
    width=100,
    height=100,
    subticks=True,
)
my_group.append(car)

car3 = Cartesian(
    x=150,
    y=10,
    width=150,
    height=100,
    xrange=(0, 160),
    axes_stroke=1,
    axes_color=0x990099,
    subticks=True,
)
my_group.append(car3)

car4 = Cartesian(
    x=30,
    y=140,
    width=80,
    height=80,
    axes_stroke=1,
    tick_color=0xFFFFFF,
    subticks=True,
)

my_group.append(car4)

car5 = Cartesian(
    x=180,
    y=140,
    width=70,
    height=70,
    xrange=(0, 120),
    yrange=(0, 90),
    tick_color=0x990099,
    axes_stroke=3,
    major_tick_length=10,
)
my_group.append(car5)

display.root_group = my_group

while True:
    pass
