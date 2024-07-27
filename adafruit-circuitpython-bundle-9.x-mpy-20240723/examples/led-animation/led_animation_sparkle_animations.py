# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
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
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import AMBER, JADE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D6
# Update to match the number of NeoPixels you have connected
pixel_num = 32

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

sparkle = Sparkle(pixels, speed=0.05, color=AMBER, num_sparkles=10)
sparkle_pulse = SparklePulse(pixels, speed=0.05, period=3, color=JADE)

animations = AnimationSequence(
    sparkle,
    sparkle_pulse,
    advance_interval=5,
    auto_clear=True,
)

while True:
    animations.animate()
