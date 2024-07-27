# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams, written for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
This example runs on an Adafruit Dotstar Feather
"""
import board
import adafruit_dotstar
from adafruit_pixel_framebuf import PixelFramebuffer

pixel_pin = board.D6
pixel_width = 12
pixel_height = 6

pixels = adafruit_dotstar.DotStar(
    board.D13,
    board.D11,
    pixel_width * pixel_height,
    brightness=0.3,
    auto_write=False,
)

pixel_framebuf = PixelFramebuffer(
    pixels,
    pixel_width,
    pixel_height,
    alternating=False,
)

pixel_framebuf.fill(0x000088)
pixel_framebuf.pixel(5, 1, 0xFFFF00)
pixel_framebuf.line(0, 0, pixel_width - 1, pixel_height - 1, 0x00FF00)
pixel_framebuf.display()
