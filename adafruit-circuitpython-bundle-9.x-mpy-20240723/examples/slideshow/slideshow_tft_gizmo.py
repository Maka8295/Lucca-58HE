# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Slideshow Example using the CircuitPlayground and TFT Gizmo

Written by Melissa LeBlanc-Williams for Adafruit Industries
"""

import board
import digitalio
from adafruit_gizmo import tft_gizmo
from adafruit_slideshow import SlideShow, PlayBackDirection

display = tft_gizmo.TFT_Gizmo()

forward_button = digitalio.DigitalInOut(board.BUTTON_A)
forward_button.switch_to_input(pull=digitalio.Pull.DOWN)
back_button = digitalio.DigitalInOut(board.BUTTON_B)
back_button.switch_to_input(pull=digitalio.Pull.DOWN)

slideshow = SlideShow(display, None, folder="/", auto_advance=False, dwell=0)

while True:
    if forward_button.value:
        slideshow.direction = PlayBackDirection.FORWARD
        slideshow.advance()
    if back_button.value:
        slideshow.direction = PlayBackDirection.BACKWARD
        slideshow.advance()
