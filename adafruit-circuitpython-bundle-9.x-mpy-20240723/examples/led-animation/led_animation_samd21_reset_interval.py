# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example shows how to reset the microcontroller to avoid the animation slowing down over time
due to the limitations of CircuitPython for the SAMD21 (M0) microcontroller. The example
animates a purple comet that bounces from end to end of the strip, and resets the board if the
specified amount of time has passed since the board was last reset.

See this FAQ for details:
https://learn.adafruit.com/circuitpython-led-animations/faqs#on-the-samd21-non-express-board-why-does-my-animation-slow-down-if-i-leave-it-running-for-a-while-3074335-3

For QT Py Haxpress and a NeoPixel strip. Update pixel_pin and pixel_num to match your wiring if
using a different board or form of NeoPixels.

This example will run on SAMD21 (M0) Express boards (such as Circuit Playground Express or QT Py
Haxpress), but not on SAMD21 non-Express boards (such as QT Py or Trinket).
"""
import time
import microcontroller
import board
import neopixel

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import PURPLE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.A3
# Update to match the number of NeoPixels you have connected
pixel_num = 30

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

comet = Comet(pixels, speed=0.02, color=PURPLE, tail_length=10, bounce=True)

while True:
    comet.animate()

    if time.monotonic() > 3600:  # After an hour passes, reset the board.
        microcontroller.reset()  # pylint: disable=no-member
