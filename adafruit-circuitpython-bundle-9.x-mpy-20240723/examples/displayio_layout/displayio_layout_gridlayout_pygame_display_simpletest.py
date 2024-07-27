# SPDX-FileCopyrightText: 2021 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Make a GridLayout with some Labels in it's cells.
Displayed with Blinka_Displayio_PyGameDisplay

Requires: https://github.com/FoamyGuy/Blinka_Displayio_PyGameDisplay
"""
import displayio
import terminalio
from adafruit_display_text import label
from blinka_displayio_pygamedisplay import PyGameDisplay


# Make the display context. Change size if you want
from adafruit_displayio_layout.layouts.grid_layout import GridLayout

display = PyGameDisplay(width=320, height=240)
main_group = displayio.Group()
display.root_group = main_group

layout = GridLayout(
    x=10,
    y=10,
    width=320,
    height=100,
    grid_size=(2, 2),
    cell_padding=8,
)
_labels = []

_labels.append(
    label.Label(
        terminalio.FONT, scale=2, x=0, y=0, text="Hello", background_color=0x770077
    )
)
layout.add_content(_labels[0], grid_position=(0, 0), cell_size=(1, 1))
_labels.append(
    label.Label(
        terminalio.FONT, scale=2, x=0, y=0, text="World", background_color=0x007700
    )
)
layout.add_content(_labels[1], grid_position=(1, 0), cell_size=(1, 1))
_labels.append(label.Label(terminalio.FONT, scale=2, x=0, y=0, text="Hello"))
layout.add_content(_labels[2], grid_position=(0, 1), cell_size=(1, 1))
_labels.append(label.Label(terminalio.FONT, scale=2, x=0, y=0, text="Grid"))
layout.add_content(_labels[3], grid_position=(1, 1), cell_size=(1, 1))

main_group.append(layout)
while display.running:
    pass
