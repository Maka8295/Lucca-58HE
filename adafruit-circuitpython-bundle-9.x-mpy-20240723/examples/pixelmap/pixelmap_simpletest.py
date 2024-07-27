# SPDX-FileCopyrightText: 2022 Tim Cocks for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example shows usage of the PixelMap helper to easily treat a single strip as a horizontal or
vertical grid for animation purposes.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels. Note that if you are using a number of pixels other than 32, you
will need to alter the PixelMap values as well for this example to work.

This example does not work on SAMD21 (M0) boards.
"""
import time
import board
import neopixel
from adafruit_pixelmap import PixelMap, horizontal_strip_gridmap

# board.NEOPIXEL is the pin on the NeoTrellis M4.
# Update to match the pin that your neopixels are connected to.
pixel_pin = board.NEOPIXEL

# Update to match the number of NeoPixels you have connected
pixel_num = 32

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.1, auto_write=True)

pixel_wing_vertical = PixelMap.vertical_lines(
    pixels, 8, 4, horizontal_strip_gridmap(8, alternating=False)
)
pixel_wing_horizontal = PixelMap.horizontal_lines(
    pixels, 8, 4, horizontal_strip_gridmap(8, alternating=False)
)

for i, row in enumerate(pixel_wing_horizontal):
    pixels.fill(0x00000)
    pixel_wing_horizontal[i] = 0x00FF00
    time.sleep(0.3)

for i, col in enumerate(pixel_wing_vertical):
    pixels.fill(0x00000)
    pixel_wing_vertical[i] = 0xFF00FF
    time.sleep(0.3)

while True:
    pass
