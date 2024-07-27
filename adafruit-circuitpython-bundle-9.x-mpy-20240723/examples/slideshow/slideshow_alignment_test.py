# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example runs best on a PyPortal or other device with a
display larger than 128px in both directions.

This example cycles through 4 different images and moves
them around to different positions on the screen each
time it updates by using the alignment feature.

You must copy the images/ directory onto your CIRCUITPY drive.
"""
import board
from adafruit_slideshow import (
    PlayBackOrder,
    SlideShow,
    VerticalAlignment,
    HorizontalAlignment,
)

# pylint: disable=no-member

# Create the slideshow object that plays through once alphabetically.
slideshow = SlideShow(
    board.DISPLAY,
    None,
    folder="/images/",
    loop=True,
    order=PlayBackOrder.ALPHABETICAL,
)

aligns = [
    (VerticalAlignment.TOP, HorizontalAlignment.CENTER),
    (VerticalAlignment.TOP, HorizontalAlignment.RIGHT),
    (VerticalAlignment.CENTER, HorizontalAlignment.LEFT),
    (VerticalAlignment.CENTER, HorizontalAlignment.CENTER),
    (VerticalAlignment.CENTER, HorizontalAlignment.RIGHT),
    (VerticalAlignment.BOTTOM, HorizontalAlignment.LEFT),
    (VerticalAlignment.BOTTOM, HorizontalAlignment.CENTER),
    (VerticalAlignment.BOTTOM, HorizontalAlignment.RIGHT),
    (VerticalAlignment.TOP, HorizontalAlignment.LEFT),
]
i = 0
slideshow.h_align = aligns[i][1]
slideshow.v_align = aligns[i][0]
i += 1

prev_img = slideshow.current_slide_name
while slideshow.update():
    cur_img = slideshow.current_slide_name
    if prev_img != cur_img:
        slideshow.h_align = aligns[i][1]
        slideshow.v_align = aligns[i][0]
        i += 1
        if i >= len(aligns):
            i = 0

    prev_img = cur_img
