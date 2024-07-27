# SPDX-FileCopyrightText: 2021 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Make green and purple rectangles and then update the color
and text values of the labels using the get_cell() function.
"""
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

# Make the display context
main_group = displayio.Group()
display.root_group = main_group

layout = GridLayout(
    x=10,
    y=10,
    width=200,
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

layout.get_cell((0, 0)).text = "Happy"
layout.get_cell((1, 0)).text = "Circuit"

layout.get_cell((0, 1)).text = "Python"
layout.get_cell((1, 1)).text = "Day"

layout.get_cell((0, 1)).background_color = 0x007700
layout.get_cell((1, 1)).background_color = 0x770077

while True:
    pass
