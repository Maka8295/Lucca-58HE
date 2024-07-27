# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example uses adafruit_display_text.label to display text using a custom font
loaded by adafruit_bitmap_font.
Adapted for use on MagTag
"""
import time
import board
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

# use built in display (MagTag, PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY
# wait until we can refresh the display
time.sleep(display.time_to_refresh)

# try uncommenting different font files if you like
font_file = "fonts/LeagueSpartan-Bold-16.bdf"
# font_file = "fonts/Junction-regular-24.pcf"

# Set text, font, and color
text = "HELLO WORLD\nbitmap_font example"
font = bitmap_font.load_font(font_file)
color = 0xFFFFFF
background_color = 0x999999

# Create the tet label
text_area = label.Label(
    font,
    text=text,
    color=color,
    background_color=background_color,
    padding_top=3,
    padding_bottom=3,
    padding_right=4,
    padding_left=4,
)
text_area.line_spacing = 1.0
# Set the location
text_area.x = 20
text_area.y = 20

# Show it and refresh
display.root_group = text_area
display.refresh()
while True:
    pass
