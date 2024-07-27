# SPDX-FileCopyrightText: 2022 Jeff Epler
#
# SPDX-License-Identifier: Unlicense

import time
import board
from adafruit_neopxl8 import NeoPxl8

# Customize for your strands here
num_strands = 8
strand_length = 30
first_led_pin = board.NEOPIXEL0

num_pixels = num_strands * strand_length

# Make the object to control the pixels
pixels = NeoPxl8(
    first_led_pin,
    num_pixels,
    num_strands=num_strands,
    auto_write=False,
    brightness=1.00,
)

while True:
    for i in range(num_pixels):
        pixels[i] = 0x00_01_00
        pixels[i - 8] = 0x00_00_00
        pixels.show()
        time.sleep(1e-3)
