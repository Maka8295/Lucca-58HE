# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Simple FancyLED example for Circuit Playground Express
"""

from adafruit_circuitplayground.express import cpx
import adafruit_fancyled.adafruit_fancyled as fancy

cpx.pixels.auto_write = False  # Refresh pixels only when we say
cpx.pixels.brightness = 1.0  # We'll use FancyLED's brightness controls

# Declare a 4-element color palette, this one happens to be a
# 'blackbody' palette -- good for heat maps and firey effects.
palette = [
    fancy.CRGB(1.0, 1.0, 1.0),  # White
    fancy.CRGB(1.0, 1.0, 0.0),  # Yellow
    fancy.CRGB(1.0, 0.0, 0.0),  # Red
    fancy.CRGB(0.0, 0.0, 0.0),
]  # Black

offset = 0  # Positional offset into color palette to get it to 'spin'
levels = (0.25, 0.3, 0.15)  # Color balance / brightness for gamma function

while True:
    for i in range(10):
        # Load each pixel's color from the palette using an offset, run it
        # through the gamma function, pack RGB value and assign to pixel.
        color = fancy.palette_lookup(palette, offset + i / 10)
        color = fancy.gamma_adjust(color, brightness=levels)
        cpx.pixels[i] = color.pack()
    cpx.pixels.show()

    offset += 0.033  # Bigger number = faster spin
