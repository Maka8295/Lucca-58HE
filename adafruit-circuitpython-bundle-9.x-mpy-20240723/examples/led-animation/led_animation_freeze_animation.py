# SPDX-FileCopyrightText: 2021 Alec Delaney
# SPDX-License-Identifier: MIT

"""
This example uses Pulse animation along with a connected push button to freeze
the animation permanently when pressed

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.
"""
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull

from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import RED

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

pulse_animation = Pulse(pixels, speed=0.1, period=1, color=RED)

while True:
    pulse_animation.animate()

    # Pressing the button pauses the animation permanently
    if not button.value:
        pulse_animation.freeze()
