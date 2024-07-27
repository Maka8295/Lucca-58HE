# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams, written for Adafruit Industries
# SPDX-License-Identifier: MIT
import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

pixel_pin = board.D6
pixel_width = 32
pixel_height = 8

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_width * pixel_height,
    brightness=0.1,
    auto_write=False,
)

pixel_framebuf = PixelFramebuffer(
    pixels, pixel_width, pixel_height, orientation=VERTICAL, rotation=2
)

pixel_framebuf.fill(0x000088)
pixel_framebuf.pixel(2, 1, 0xFFFF00)
pixel_framebuf.line(0, 0, pixel_width - 1, pixel_height - 1, 0x00FF00)
pixel_framebuf.line(0, pixel_height - 1, pixel_width - 1, 0, 0x00FF00)
pixel_framebuf.circle(pixel_width // 2 - 1, pixel_height // 2 - 1, 4, 0xFF0000)
pixel_framebuf.rect(1, 2, 8, pixel_height - 3, 0xFF00FF)
pixel_framebuf.display()
