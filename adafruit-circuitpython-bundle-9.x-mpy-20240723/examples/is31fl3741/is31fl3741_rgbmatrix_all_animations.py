# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Neradoc https://neradoc.me
# SPDX-License-Identifier: MIT
"""
This example repeatedly displays all available animations
on the IS31FL3741 13x9 RGB Matrix, at a five second interval.
"""
import board
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
from adafruit_is31fl3741 import PREFER_BUFFER
from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT
from adafruit_is31fl3741.is31fl3741_pixelbuf import IS31FL3741_PixelBuf

# i2c = board.I2C()
i2c = board.STEMMA_I2C()

########################################################################
# Instantiate the nice IS31FL3741
########################################################################

is31 = Adafruit_RGBMatrixQT(i2c, allocate=PREFER_BUFFER)
is31.set_led_scaling(0xFF)
is31.global_current = 0xFF
is31.enable = True

########################################################################
# Setup the mapping and PixelBuf instance
########################################################################

WIDTH = 13
HEIGHT = 9
LEDS_MAP = tuple(
    (
        address
        for y in range(HEIGHT)
        for x in range(WIDTH)
        for address in Adafruit_RGBMatrixQT.pixel_addrs(x, y)
    )
)
pixels = IS31FL3741_PixelBuf(is31, LEDS_MAP, init=False, auto_write=False)

########################################################################
# Run animations
########################################################################

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
