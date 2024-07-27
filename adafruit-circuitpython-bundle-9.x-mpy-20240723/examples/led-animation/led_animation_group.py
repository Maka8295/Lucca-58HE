# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example shows three different ways to use AnimationGroup: syncing two animations, displaying
two animations at different speeds, and displaying two animations sequentially, across two separate
pixel objects such as the built-in NeoPixels on a Circuit Playground Bluefruit and a NeoPixel strip.

This example is written for Circuit Playground Bluefruit and a 30-pixel NeoPixel strip connected to
pad A1. It does not work on Circuit Playground Express.
"""
import board
import neopixel
from adafruit_circuitplayground import cp

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase

from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.sequence import AnimationSequence

from adafruit_led_animation import color

strip_pixels = neopixel.NeoPixel(board.A1, 30, brightness=0.5, auto_write=False)
cp.pixels.brightness = 0.5

animations = AnimationSequence(
    # Synchronized to 0.5 seconds. Ignores the second animation setting of 3 seconds.
    AnimationGroup(
        Blink(cp.pixels, 0.5, color.CYAN),
        Blink(strip_pixels, 3.0, color.AMBER),
        sync=True,
    ),
    # Different speeds
    AnimationGroup(
        Comet(cp.pixels, 0.1, color.MAGENTA, tail_length=5),
        Comet(strip_pixels, 0.01, color.MAGENTA, tail_length=15),
    ),
    # Different animations
    AnimationGroup(
        Blink(cp.pixels, 0.5, color.JADE),
        Comet(strip_pixels, 0.05, color.TEAL, tail_length=15),
    ),
    # Sequential animations on the built-in NeoPixels then the NeoPixel strip
    Chase(cp.pixels, 0.05, size=2, spacing=3, color=color.PURPLE),
    Chase(strip_pixels, 0.05, size=2, spacing=3, color=color.PURPLE),
    advance_interval=3.0,
    auto_clear=True,
    auto_reset=True,
)

while True:
    animations.animate()
