# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example uses adafruit_display_text.label to display text using a custom font
loaded by adafruit_bitmap_font
"""

import board
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# use built in display (MagTag, PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

# try uncommenting different font files if you like
font_file = "fonts/LeagueSpartan-Bold-16.bdf"
# font_file = "fonts/Junction-regular-24.pcf"

# Set text, font, and color
text = "HELLO WORLD"
font = bitmap_font.load_font(font_file)
color = 0xFF00FF

# Create the tet label
text_area = label.Label(font, text=text, color=color)

# Set the location
text_area.x = 20
text_area.y = 20

# Show it
display.root_group = text_area

while True:
    pass
