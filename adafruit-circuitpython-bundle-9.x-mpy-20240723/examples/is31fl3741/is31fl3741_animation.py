# SPDX-FileCopyrightText: 2021 Rose Hooper
# SPDX-License-Identifier: MIT

import board
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.color import PURPLE
from adafruit_led_animation.sequence import AnimationSequence

from adafruit_is31fl3741.adafruit_ledglasses import MUST_BUFFER, LED_Glasses
from adafruit_is31fl3741.led_glasses_animation import LED_Glasses_Animation

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
glasses = LED_Glasses(i2c, allocate=MUST_BUFFER)
glasses.set_led_scaling(255)
glasses.global_current = 0xFE
glasses.enable = True

pixels = LED_Glasses_Animation(glasses)

anim1 = RainbowComet(pixels, 0.05, tail_length=24, ring=True)
anim2 = Sparkle(pixels, 0.05, PURPLE)
anim3 = ColorCycle(pixels, 0.03)
group = AnimationSequence(
    anim1, anim2, anim3, advance_interval=4, auto_reset=True, auto_clear=True
)
while True:
    group.animate()
