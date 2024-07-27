# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw 8 colored
labels. Useful for testing the color settings on an unknown display.
"""

import board
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_st7735r import ST7735R

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D5
tft_dc = board.D6

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D9)

display = ST7735R(
    display_bus, width=160, height=80, colstart=24, rotation=270, bgr=False
)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(160, 80, 1)
color_palette = displayio.Palette(1)
# write some text in each font color, rgb, cmyk
color_palette[0] = 0x111111  # light grey

text_group_left = displayio.Group(scale=1, x=0, y=6)
text_area_red = label.Label(terminalio.FONT, text="RED", color=0xFF0000)
text_area_green = label.Label(terminalio.FONT, text="\nGREEN", color=0x00FF00)
text_area_blue = label.Label(terminalio.FONT, text="\n\nBLUE", color=0x0000FF)
text_area_white = label.Label(terminalio.FONT, text="\n\n\nWHITE", color=0xFFFFFF)
text_group_left.append(text_area_red)
text_group_left.append(text_area_green)
text_group_left.append(text_area_blue)
text_group_left.append(text_area_white)
splash.append(text_group_left)

text_group_right = displayio.Group(scale=1, x=80, y=6)
text_area_cyan = label.Label(terminalio.FONT, text="CYAN", color=0x00FFFF)
text_group_right.append(text_area_cyan)
text_area_magenta = label.Label(terminalio.FONT, text="\nMAGENTA", color=0xFF00FF)
text_group_right.append(text_area_magenta)
text_area_yellow = label.Label(terminalio.FONT, text="\n\nYELLOW", color=0xFFFF00)
text_group_right.append(text_area_yellow)
text_area_black = label.Label(terminalio.FONT, text="\n\n\nBLACK", color=0x000000)
text_group_right.append(text_area_black)
splash.append(text_group_right)

while True:
    pass
