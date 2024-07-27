# SPDX-FileCopyrightText: 2022 David Glaude (based on 2021 ladyada for Adafruit Industries)
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, and some white text.
Customized version of displayio_ssd1306_simpletest.py for 64x32
"""

import board
import displayio

# Compatibility with both CircuitPython 8.x.x and 9.x.x.
# Remove after 8.x.x is no longer a supported release.
try:
    from i2cdisplaybus import I2CDisplayBus
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus

import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

displayio.release_displays()

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

display_bus = I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=64, height=32)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(64, 32, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

## Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(62, 30, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black

inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
splash.append(inner_sprite)

TEXT1 = "Hello"
text_area = label.Label(terminalio.FONT, text=TEXT1, color=0xFFFFFF, x=2, y=6)
splash.append(text_area)

TEXT2 = "World"
text_area = label.Label(terminalio.FONT, text=TEXT2, color=0xFFFFFF, x=32, y=15)
splash.append(text_area)

TEXT3 = "9876543210"
text_area = label.Label(terminalio.FONT, text=TEXT3, color=0xFFFFFF, x=2, y=24)
splash.append(text_area)

while True:
    pass
