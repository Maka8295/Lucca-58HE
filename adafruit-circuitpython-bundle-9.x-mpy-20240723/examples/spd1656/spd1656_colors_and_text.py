# SPDX-FileCopyrightText: Copyright (c) 2023 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Colors and Text script for 5.6" 600x448 7-color ACeP display.
Draw a border and screen filled with color and layer text on top
of it.
"""
# pylint: disable=no-member

import board
import displayio
import terminalio
import bitmaptools
from adafruit_display_text.bitmap_label import Label
import fourwire
import adafruit_spd1656


displayio.release_displays()

# This pinout works on a Feather RP2040 and may need to be altered for other boards.
spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10
epd_reset = board.D11
epd_busy = board.D12

display_bus = fourwire.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)

display = adafruit_spd1656.SPD1656(
    display_bus, width=600, height=448, busy_pin=epd_busy
)

g = displayio.Group()

bmp = displayio.Bitmap(display.width, display.height, 7)
p = displayio.Palette(7)
p[0] = 0xFFFFFF
p[1] = 0x000000
p[2] = 0x0000FF
p[3] = 0x00FF00
p[4] = 0xFF0000
p[5] = 0xFFFF00
p[6] = 0xFFA500

bmp.fill(2)

bitmaptools.fill_region(bmp, 40, 40, display.width - 40, display.height - 40, 3)
tg = displayio.TileGrid(bitmap=bmp, pixel_shader=p)
g.append(tg)

lbl = Label(terminalio.FONT, text="Hello World", color=0xFFFFFF, scale=3)
lbl.anchor_point = (0.5, 0.5)
lbl.anchored_position = (display.width // 2, display.height // 2)
g.append(lbl)

display.root_group = g
display.refresh()

while True:
    pass
