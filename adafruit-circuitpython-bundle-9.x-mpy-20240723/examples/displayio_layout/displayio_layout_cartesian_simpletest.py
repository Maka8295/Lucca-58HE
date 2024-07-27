# SPDX-FileCopyrightText: 2021 Jose David M.
#
# SPDX-License-Identifier: MIT
#############################
"""
This is a basic demonstration of a Cartesian widget.
"""

import time
import board
import displayio
import terminalio
from adafruit_displayio_layout.widgets.cartesian import Cartesian

# Fonts used for the Dial tick labels
tick_font = terminalio.FONT

display = board.DISPLAY  # create the display on the PyPortal or Clue (for example)
# otherwise change this to setup the display
# for display chip driver and pinout you have (e.g. ILI9341)


# Create a Cartesian widget
my_plane = Cartesian(
    x=150,  # x position for the plane
    y=100,  # y plane position
    width=100,  # display width
    height=100,  # display height
    axes_color=0xFFFFFF,  # axes line color
    axes_stroke=2,  # axes lines width in pixels
    tick_color=0xFFFFFF,  # ticks color
    major_tick_stroke=1,  # ticks width in pixels
    major_tick_length=5,  # ticks length in pixels
    tick_label_font=tick_font,  # the font used for the tick labels
    font_color=0xFFFFFF,  # ticks line color
)

my_group = displayio.Group()
my_group.append(my_plane)
display.root_group = my_group  # add high level Group to the display

posx = 0
posy = 0

while True:
    for i in range(0, 90, 2):
        my_plane.update_pointer(i, i)
        time.sleep(0.5)
