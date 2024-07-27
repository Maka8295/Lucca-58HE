# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams, written for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
This example runs on an Adafruit NeoPixel Feather
"""
import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer

pixel_pin = board.D6
pixel_width = 8
pixel_height = 4

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height,
    brightness=0.1,
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
