# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import pwmio
import touchio
from adafruit_slideshow import SlideShow, PlayBackDirection

# pylint: disable=no-member

forward_button = touchio.TouchIn(board.TOUCH4)
back_button = touchio.TouchIn(board.TOUCH1)

brightness_up = touchio.TouchIn(board.TOUCH3)
brightness_down = touchio.TouchIn(board.TOUCH2)

slideshow = SlideShow(
    board.DISPLAY,
    pwmio.PWMOut(board.TFT_BACKLIGHT),
    folder="/",
    auto_advance=False,
    dwell=0,
)

while True:
    if forward_button.value:
        slideshow.direction = PlayBackDirection.FORWARD
        slideshow.advance()
    if back_button.value:
        slideshow.direction = PlayBackDirection.BACKWARD
        slideshow.advance()

    if brightness_up.value:
        slideshow.brightness += 0.001
    elif brightness_down.value:
        slideshow.brightness -= 0.001
