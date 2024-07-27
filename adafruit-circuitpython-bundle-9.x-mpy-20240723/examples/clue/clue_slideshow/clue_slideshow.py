# SPDX-FileCopyrightText: 2019 Kattni Rembor, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Display a series of bitmaps using the buttons to advance through the list. To use: place
supported bitmap files on your CIRCUITPY drive, then press the buttons on your CLUE to advance
through them.

Requires the Adafruit CircuitPython Slideshow library!"""

from adafruit_slideshow import SlideShow, PlayBackDirection
from adafruit_clue import clue

slideshow = SlideShow(clue.display, auto_advance=False)

while True:
    if clue.button_b:
        slideshow.direction = PlayBackDirection.FORWARD
        slideshow.advance()
    if clue.button_a:
        slideshow.direction = PlayBackDirection.BACKWARD
        slideshow.advance()
