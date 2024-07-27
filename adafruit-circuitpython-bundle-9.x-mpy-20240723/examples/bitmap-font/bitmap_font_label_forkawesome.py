# SPDX-FileCopyrightText: 2021 Tim Cocks
# SPDX-License-Identifier: MIT

"""
This example uses adafruit_display_text.label to display fork awesome
icons.

More info here: https://emergent.unpythonic.net/01606790241
"""

import board
from bitmap_font_forkawesome_icons import microchip, python, terminal
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# use built in display (MagTag, PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

font_file = "fonts/forkawesome-42.pcf"

# Set text, font, and color
text = "{}  {}  {}".format(terminal, python, microchip)
font = bitmap_font.load_font(font_file)
color = 0xFF00FF

# Create the tet label
text_area = label.Label(font, text=text, color=color)

# Set the location
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (display.width // 2, display.height // 2)

# Show it
display.root_group = text_area

while True:
    pass
