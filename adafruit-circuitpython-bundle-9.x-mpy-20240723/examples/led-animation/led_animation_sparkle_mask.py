# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries, karan bhatia
# SPDX-License-Identifier: MIT
"""
This example uses AnimationsSequence to display multiple animations in sequence, at a five second
interval.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.
"""
import board
import neopixel

from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import JADE, AQUA, PINK

# Update to match the pin connected to your NeoPixels
pixel_pin = board.A1
# Update to match the number of NeoPixels you have connected
pixel_num = 64
# fmt: off
heart_mask = [     1,  2,          5,  6,
              8,   9, 10, 11, 12, 13, 14, 15,
              16, 17, 18, 19, 20, 21, 22, 23,
              24, 25, 26, 27, 28, 29, 30, 31,
                  33, 34, 35, 36, 37, 38,
                      42, 43, 44, 45,
                          51, 52]
unheart_mask = [0,           3,  4,         7,



                32,                        39,
                40, 41,                46, 47,
                48, 49, 50,        53, 54, 55,
                56, 57, 58, 59, 60, 61, 62, 63]
# fmt: on
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.9, auto_write=False)

animations = AnimationSequence(
    Sparkle(pixels, speed=0.05, color=JADE, num_sparkles=1, mask=unheart_mask),
    Sparkle(pixels, speed=0.05, color=AQUA, num_sparkles=1),
    Sparkle(pixels, speed=0.05, color=PINK, num_sparkles=1, mask=heart_mask),
    advance_interval=5,
    auto_clear=False,
)

while True:
    animations.animate()
