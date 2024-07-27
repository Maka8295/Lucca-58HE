# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

# Make the display context
splash = displayio.Group()
display.root_group = splash

# Make a background color fill
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
splash.append(bg_sprite)
##########################################################################

splash.append(Line(5, 74, 10, 110, 0x000000))
splash.append(Line(15, 74, 20, 110, 0x000000))
splash.append(Line(25, 74, 30, 110, 0x000000))
splash.append(Line(35, 74, 40, 110, 0x000000))

# Draw star
polygon = Polygon(
    [
        (255, 40),
        (262, 62),
        (285, 62),
        (265, 76),
        (275, 100),
        (255, 84),
        (235, 100),
        (245, 76),
        (225, 62),
        (248, 62),
    ],
    outline=0x000000,
)
splash.append(polygon)

triangle = Triangle(170, 20, 140, 90, 210, 100, fill=0x999999, outline=0x000000)
splash.append(triangle)

rect = Rect(80, 20, 41, 41, fill=0x999999, outline=0x666666)
splash.append(rect)

circle = Circle(100, 100, 20, fill=0xFFFFFF, outline=0x000000)
splash.append(circle)

rect2 = Rect(70, 85, 61, 30, outline=0x0, stroke=3)
splash.append(rect2)

roundrect = RoundRect(10, 10, 61, 51, 10, fill=0x666666, outline=0x000000, stroke=6)
splash.append(roundrect)

display.refresh()
while True:
    pass
