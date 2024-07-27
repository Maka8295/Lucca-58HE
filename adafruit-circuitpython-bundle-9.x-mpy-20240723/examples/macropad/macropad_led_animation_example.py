# SPDX-FileCopyrightText: 2021 Tim Cocks
# SPDX-License-Identifier: MIT

"""
This simpletest example displays the Blink animation on the
MacroPad neopixels
"""
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.color import BLUE
from adafruit_macropad import MacroPad

macropad = MacroPad()

blink = Blink(macropad.pixels, speed=0.5, color=BLUE)

while True:
    blink.animate()
