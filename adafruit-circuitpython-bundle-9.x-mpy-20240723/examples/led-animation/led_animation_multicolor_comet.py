# SPDX-FileCopyrightText: 2022 Tim Cocks
#
# SPDX-License-Identifier: MIT
"""
This example animates a red, yellow, and green gradient comet that bounces
from end to end of the strip.

For QT Py Haxpress and a NeoPixel strip. Update pixel_pin and pixel_num to match your wiring if
using a different board or form of NeoPixels.

This example will run on SAMD21 (M0) Express boards (such as Circuit Playground Express or QT Py
Haxpress), but not on SAMD21 non-Express boards (such as QT Py or Trinket).
"""
import board
import neopixel
from adafruit_led_animation.animation.multicolor_comet import MulticolorComet

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D9
# Update to match the number of NeoPixels you have connected
pixel_num = 96
brightness = 0.02

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_num,
    brightness=brightness,
    auto_write=True,
    pixel_order=neopixel.RGB,
)

comet_colors = [
    0xFF0000,
    0xFD2000,
    0xF93E00,
    0xF45B00,
    0xEC7500,
    0xE28D00,
    0xD5A200,
    0xC6B500,
    0xB5C600,
    0xA2D500,
    0x8DE200,
    0x75EC00,
    0x5BF400,
    0x3EF900,
    0x20FD00,
    0x00FF00,
]


comet = MulticolorComet(
    pixels,
    colors=comet_colors,
    speed=0.01,
    tail_length=20,
    bounce=True,
    ring=False,
    reverse=False,
)

while True:
    comet.animate()
