# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example illustrates how to use the wrap_text_to_lines
helper function.
"""
import board
import terminalio
from adafruit_display_text import label, wrap_text_to_lines

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

text = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
    "sed do eiusmod tempor incididunt ut labore et dolore magna "
    "aliqua. Ut enim ad minim veniam, quis nostrud exercitation "
    "ullamco laboris nisi ut aliquip ex ea commodo consequat."
)
text = "\n".join(wrap_text_to_lines(text, 28))
text_area = label.Label(terminalio.FONT, text=text)
text_area.x = 10
text_area.y = 10
display.root_group = text_area
while True:
    pass
