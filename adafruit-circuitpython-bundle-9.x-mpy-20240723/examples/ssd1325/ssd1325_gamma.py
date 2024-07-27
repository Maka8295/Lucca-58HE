# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import displayio
import adafruit_ssd1325

# Support both 8.x.x and 9.x.x. Change when 8.x.x is discontinued as a stable release.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

displayio.release_displays()

spi = board.SPI()
oled_cs = board.D5
oled_dc = board.D6
oled_reset = board.D9

display_bus = FourWire(
    spi, command=oled_dc, chip_select=oled_cs, reset=oled_reset, baudrate=1000000
)
time.sleep(1)
display = adafruit_ssd1325.SSD1325(display_bus, width=128, height=64)

g = displayio.Group()
dimension = min(display.width, display.height)
color_count = 16
gamma_pattern = displayio.Bitmap(dimension, dimension, color_count)
gamma_palette = displayio.Palette(color_count)
t = displayio.TileGrid(gamma_pattern, pixel_shader=gamma_palette)

pixels_per_step = dimension // color_count

for i in range(dimension):
    if i % pixels_per_step == 0:
        continue
    gamma_pattern[i, i] = i // pixels_per_step

for i in range(color_count):
    component = i * 255 // (color_count - 1)
    print(component)
    gamma_palette[i] = component << 16 | component << 8 | component

g.append(t)

display.root_group = g

time.sleep(10)
