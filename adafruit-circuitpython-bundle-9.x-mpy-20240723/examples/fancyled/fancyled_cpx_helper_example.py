# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" FancyLED example for Circuit Playground Express using fastled_helpers
"""

from adafruit_circuitplayground.express import cpx
import adafruit_fancyled.fastled_helpers as helper

cpx.pixels.auto_write = False  # Refresh pixels only when we say

# A dynamic gradient palette is a compact way of representing a palette with
# non-equal spacing between elements.  This one's a blackbody palette with a
# longer red 'tail'.  The helper functions let us declare this as a list of
# bytes, so they're easier to copy over from existing FastLED projects.
# fmt: off
heatmap_gp = bytes([
    0, 255, 255, 255,  # White
    64, 255, 255, 0,  # Yellow
    128, 255, 0, 0,  # Red
    255, 0, 0, 0])  # Black
# fmt: on

# Convert the gradient palette into a normal palette w/16 elements:
palette = helper.loadDynamicGradientPalette(heatmap_gp, 16)

offset = 0  # Positional offset into color palette to get it to 'spin'

while True:
    for i in range(10):
        # Load each pixel's color from the palette.  FastLED uses 16-step
        # in-between blending...so for a 16-color palette, there's 256
        # steps total.  With 10 pixels, multiply the pixel index by 25.5
        # (and add our offset) to get FastLED-style palette position.
        color = helper.ColorFromPalette(palette, int(offset + i * 25.5), blend=True)
        # Apply gamma using the FastLED helper syntax
        color = helper.applyGamma_video(color)
        # 'Pack' color and assign to NeoPixel #i
        cpx.pixels[i] = color.pack()
    cpx.pixels.show()

    offset += 8  # Bigger number = faster spin
