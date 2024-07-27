# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example loads a font and uses it to print an
ASCII art representation of the given string specimen
"""

from adafruit_bitmap_font import bitmap_font  # pylint: disable=wrong-import-position

# you can change this to a different bdf or pcf font file
font_file = "fonts/LeagueSpartan-Bold-16.bdf"

# you can change the string that will get printed here
message = "<3 Blinka"

font = bitmap_font.load_font(font_file)

_, height, _, dy = font.get_bounding_box()
font.load_glyphs(message)

for y in range(height):
    for c in message:
        glyph = font.get_glyph(ord(c))
        if not glyph:
            continue
        glyph_y = y + (glyph.height - (height + dy)) + glyph.dy
        pixels = []
        if 0 <= glyph_y < glyph.height:
            for i in range(glyph.width):
                value = glyph.bitmap[i, glyph_y]
                pixel = " "
                if value > 0:
                    pixel = "#"
                pixels.append(pixel)
        else:
            pixels = ""
        print("".join(pixels) + " " * (glyph.shift_x - len(pixels)), end="")
    print()
