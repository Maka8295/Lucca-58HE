# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Basic demonstration script will create a slideshow
object that plays through once alphabetically."""
import board
from adafruit_slideshow import PlayBackOrder, SlideShow

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

# pylint: disable=no-member

slideshow = SlideShow(
    board.DISPLAY,
    None,
    folder="/images/",
    loop=False,
    order=PlayBackOrder.ALPHABETICAL,
    dwell=10,
)

while slideshow.update():
    pass
