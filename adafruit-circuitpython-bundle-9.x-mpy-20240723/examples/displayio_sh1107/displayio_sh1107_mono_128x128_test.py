# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Based on example by Mark Roberts (mdroberts1243).

This example writes text to the display, and draws a series of squares and a rectangle.
"""

import board
import displayio

# Compatibility with both CircuitPython 8.x.x and 9.x.x.
# Remove after 8.x.x is no longer a supported release.
try:
    from i2cdisplaybus import I2CDisplayBus

    # from fourwire import FourWire
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

    # from displayio import FourWire

import terminalio
from adafruit_display_text import bitmap_label as label
from adafruit_displayio_sh1107 import SH1107, DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297

displayio.release_displays()

# For I2C
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = I2CDisplayBus(i2c, device_address=0x3D)

# For SPI:
# import busio
# spi_bus = busio.SPI(board.SCK, board.MOSI)
# display_bus = FourWire(spi_bus, command=board.D6, chip_select=board.D5, reset=board.D9)

# Width, height and rotation for Monochrome 1.12" 128x128 OLED
WIDTH = 128
HEIGHT = 128
ROTATION = 90

# Border width
BORDER = 2

display = SH1107(
    display_bus,
    width=WIDTH,
    height=HEIGHT,
    display_offset=DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297,
    rotation=ROTATION,
)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle in black
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Draw some white squares
small_bitmap = displayio.Bitmap(8, 8, 1)
small_square = displayio.TileGrid(small_bitmap, pixel_shader=color_palette, x=58, y=17)
splash.append(small_square)

medium_bitmap = displayio.Bitmap(16, 16, 1)
medium_square = displayio.TileGrid(
    medium_bitmap, pixel_shader=color_palette, x=71, y=15
)
splash.append(medium_square)

large_bitmap = displayio.Bitmap(32, 32, 1)
large_square = displayio.TileGrid(large_bitmap, pixel_shader=color_palette, x=91, y=28)
splash.append(large_square)

bottom_bitmap = displayio.Bitmap(110, 50, 1)
bottom_rectangle = displayio.TileGrid(
    bottom_bitmap, pixel_shader=color_palette, x=10, y=69
)
splash.append(bottom_rectangle)

# Draw some label text
name_text = "Monochrome 1.12in"
name_text_area = label.Label(terminalio.FONT, text=name_text, color=0xFFFFFF, x=8, y=8)
splash.append(name_text_area)
size_text = "128x128"
size_text_area = label.Label(terminalio.FONT, text=size_text, color=0xFFFFFF, x=8, y=25)
splash.append(size_text_area)
oled_text = "OLED"
oled_text_area = label.Label(
    terminalio.FONT, text=oled_text, scale=2, color=0xFFFFFF, x=9, y=44
)
splash.append(oled_text_area)

while True:
    pass
