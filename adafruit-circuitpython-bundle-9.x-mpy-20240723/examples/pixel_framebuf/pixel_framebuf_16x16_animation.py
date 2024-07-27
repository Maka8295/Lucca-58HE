# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams, written for Adafruit Industries
# SPDX-License-Identifier: MIT
import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer

pixel_pin = board.D6
pixel_width = 16
pixel_height = 16

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
    reverse_x=True,
)

text = "Welcome to CircuitPython"

while True:
    for i in range(6 * len(text) + pixel_width):
        pixel_framebuf.fill(0x000088)
        pixel_framebuf.pixel(2, 1, 0x00FFFF)
        pixel_framebuf.line(0, 0, pixel_width - 1, pixel_height - 1, 0x00FF00)
        pixel_framebuf.line(0, pixel_width - 1, pixel_height - 1, 0, 0x00FF00)
        pixel_framebuf.fill_rect(2, 3, 12, 10, 0x000000)
        pixel_framebuf.text(text, pixel_width - i, 4, 0xFFFF00)
        pixel_framebuf.rect(1, 2, 14, 12, 0xFF0000)
        pixel_framebuf.line(0, 2, 0, 14, 0x000088)
        pixel_framebuf.line(pixel_width - 1, 2, pixel_width - 1, 14, 0x000088)
        pixel_framebuf.display()
