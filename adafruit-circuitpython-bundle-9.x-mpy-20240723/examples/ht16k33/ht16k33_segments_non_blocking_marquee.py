# SPDX-FileCopyrightText: 2023 Tim Cocks for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Example that uses Non-Blocking Marquee to scroll text on 14x4 segment
while also blinking the on-board neopixel at a different rate from the
marquee scrolling.
"""

import time
import board
import neopixel
import adafruit_ht16k33.segments


i2c = board.I2C()
segment_display = adafruit_ht16k33.segments.Seg14x4(i2c)

pixel_pin = board.NEOPIXEL
pixels = neopixel.NeoPixel(pixel_pin, 1, brightness=0.1, auto_write=True)

pixels[0] = 0xFF0000
last_blink = 0
while True:
    now = time.monotonic()
    if now > last_blink + 0.3:
        if pixels[0] == (255, 0, 255):
            pixels[0] = 0x00FF00
        else:
            pixels[0] = 0xFF00FF
        last_blink = now
    segment_display.non_blocking_marquee("CircuitPython <3", delay=0.2)
