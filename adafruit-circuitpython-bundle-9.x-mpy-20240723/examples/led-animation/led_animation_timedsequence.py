# SPDX-FileCopyrightText: 2020 Gamblor21
#
# SPDX-License-Identifier: MIT
"""
Example for TimedSequence
"""
import board
import neopixel
from adafruit_led_animation.timedsequence import TimedAnimationSequence
import adafruit_led_animation.animation.comet as comet_animation
import adafruit_led_animation.animation.sparkle as sparkle_animation
import adafruit_led_animation.animation.blink as blink_animation
from adafruit_led_animation import color

strip_pixels = neopixel.NeoPixel(board.D6, 32, brightness=0.1, auto_write=False)
blink = blink_animation.Blink(strip_pixels, 0.3, color.RED)
comet = comet_animation.Comet(strip_pixels, 0.1, color.BLUE)
sparkle = sparkle_animation.Sparkle(strip_pixels, 0.05, color.GREEN)
animations = TimedAnimationSequence(blink, 2, comet, 4, sparkle, 5)
while True:
    animations.animate()
