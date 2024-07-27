# SPDX-FileCopyrightText: 2021 Alec Delaney
# SPDX-License-Identifier: MIT

"""
This example uses AnimationsSequence along with a connected push button to cycle through
two animations

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.
"""
import time
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull

from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import RED, BLUE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D6
# Update to match the number of NeoPixels you have connected
pixel_num = 32

# Update to matchpin connected to button that connect logic high when pushed
button_pin = board.D3

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)
button = DigitalInOut(button_pin)
button.direction = Direction.INPUT
button.pull = Pull.UP

solid_blue = Solid(pixels, color=BLUE)
solid_red = Solid(pixels, color=RED)
animation_sequence = AnimationSequence(solid_blue, solid_red, auto_clear=True)

while True:
    animation_sequence.animate()

    # Pressing the button pauses the animation permanently
    if not button.value:
        animation_sequence.next()
        while button.value:
            time.sleep(0.1)  # Used for button debouncing
