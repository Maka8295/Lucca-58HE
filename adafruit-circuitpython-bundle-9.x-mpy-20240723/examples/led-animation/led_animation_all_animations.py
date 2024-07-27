# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example repeatedly displays all available animations, at a five second interval.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.

This example does not work on SAMD21 (M0) boards.
"""
import board
import neopixel

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D6
# Update to match the number of NeoPixels you have connected
pixel_num = 32

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

blink = Blink(pixels, speed=0.5, color=JADE)
colorcycle = ColorCycle(pixels, speed=0.4, colors=[MAGENTA, ORANGE])
comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
pulse = Pulse(pixels, speed=0.1, period=3, color=AMBER)
sparkle = Sparkle(pixels, speed=0.1, color=PURPLE, num_sparkles=10)
solid = Solid(pixels, color=JADE)
rainbow = Rainbow(pixels, speed=0.1, period=2)
sparkle_pulse = SparklePulse(pixels, speed=0.1, period=3, color=JADE)
rainbow_comet = RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True)
rainbow_chase = RainbowChase(pixels, speed=0.1, size=3, spacing=2, step=8)
rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)
custom_color_chase = CustomColorChase(
    pixels, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
)


animations = AnimationSequence(
    comet,
    blink,
    rainbow_sparkle,
    chase,
    pulse,
    sparkle,
    rainbow,
    solid,
    rainbow_comet,
    sparkle_pulse,
    rainbow_chase,
    custom_color_chase,
    advance_interval=5,
    auto_clear=True,
)

while True:
    animations.animate()
