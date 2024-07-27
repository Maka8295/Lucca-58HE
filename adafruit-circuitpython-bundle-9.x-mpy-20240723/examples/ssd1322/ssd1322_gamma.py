# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import displayio
import adafruit_ssd1322

displayio.release_displays()

# This pinout works on a Metro and may need to be altered for other boards.
spi = busio.SPI(board.SCL, board.SDA)
tft_cs = board.D6
tft_dc = board.D9
tft_reset = board.D5

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset, baudrate=1000000
)
time.sleep(1)
display = adafruit_ssd1322.SSD1322(display_bus, width=256, height=64, colstart=28)

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
    print(hex(gamma_palette[i]))

g.append(t)

display.root_group = g

time.sleep(10)
