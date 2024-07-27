# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example displays custom color chase animations in sequence, at a six second interval.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.

This example may not work on SAMD21 (M0) boards.
"""
import board
import neopixel

from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence

# colorwheel only needed for rainbowchase example
from adafruit_led_animation.color import colorwheel

# Colors for customcolorchase examples
from adafruit_led_animation.color import PINK, GREEN, RED, BLUE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D5
# Update to match the number of NeoPixels you have connected
pixel_num = 30
brightness = 0.3

pixels = neopixel.NeoPixel(
    pixel_pin, pixel_num, brightness=brightness, auto_write=False
)

# colors default to RAINBOW as defined in color.py
custom_color_chase_rainbow = CustomColorChase(pixels, speed=0.1, size=2, spacing=3)
custom_color_chase_rainbow_r = CustomColorChase(
    pixels, speed=0.1, size=3, spacing=3, reverse=True
)

# Example with same colors as RainbowChase
steps = 30
# This was taken from rainbowchase.py
rainbow_colors = [colorwheel(n % 256) for n in range(0, 512, steps)]
# Now use rainbow_colors with CustomColorChase
custom_color_chase_rainbowchase = CustomColorChase(
    pixels, speed=0.1, colors=rainbow_colors, size=2, spacing=3
)

custom_color_chase_bgp = CustomColorChase(
    pixels, speed=0.1, colors=[BLUE, GREEN, PINK], size=3, spacing=2
)

# Can use integer values for color, 0 is black
custom_color_chase_br = CustomColorChase(
    pixels, speed=0.1, colors=[BLUE, 0, RED, 0], size=2, spacing=0
)

animations = AnimationSequence(
    custom_color_chase_rainbow,
    custom_color_chase_rainbow_r,
    custom_color_chase_rainbowchase,
    custom_color_chase_bgp,
    custom_color_chase_br,
    advance_interval=6,
    auto_clear=True,
)

while True:
    animations.animate()
