# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Touch paint example for HX83570 + FT5336 TFT Breakout
"""

import board
import displayio
from adafruit_hx8357 import HX8357
import adafruit_ft5336

displayio.release_displays()

spi = board.SPI()
# for eyespi bff
# tft_cs = board.TX
# tft_dc = board.RX
# else:
tft_cs = board.D9
tft_dc = board.D10

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
# display is rotated to align x, y with touch screen x, y
display = HX8357(display_bus, width=320, height=480, rotation=90)

i2c = board.I2C()  # uses board.SCL and board.SDA
touch = adafruit_ft5336.Adafruit_FT5336(i2c)

pixel_size = 10
palette_width = 45
palette_height = 320 // 8

splash = displayio.Group()
display.root_group = splash

bitmap = displayio.Bitmap(320, 480, 8)
color_palette = displayio.Palette(8)
color_palette[0] = 0x000000
color_palette[1] = 0xFF0000
color_palette[2] = 0xFFFF00
color_palette[3] = 0x00FF00
color_palette[4] = 0x00FFFF
color_palette[5] = 0x0000FF
color_palette[6] = 0xFF00FF
color_palette[7] = 0xFFFFFF

tile_grid = displayio.TileGrid(bitmap, pixel_shader=color_palette)
# tilegrid is flipped to align x, y with touch screen x, y
tile_grid.flip_y = True
tile_grid.flip_x = True

splash.append(tile_grid)

display.root_group = splash

current_color = 7

for i in range(palette_width):
    for j in range(palette_height):
        bitmap[j + palette_height, i] = 1
        bitmap[j + palette_height * 2, i] = 2
        bitmap[j + palette_height * 3, i] = 3
        bitmap[j + palette_height * 4, i] = 4
        bitmap[j + palette_height * 5, i] = 5
        bitmap[j + palette_height * 6, i] = 6
        bitmap[j + palette_height * 7, i] = 0

while True:
    if touch.touched:
        try:
            for t in touch.points:
                x = t[0]
                y = t[1]
                print(x, y)
                if not 0 <= x < display.width or not 0 <= y < display.height:
                    continue  # Skip out of bounds touches
                if y < palette_width:
                    current_color = bitmap[x, y]
                else:
                    for i in range(pixel_size):
                        for j in range(pixel_size):
                            x_pixel = x - (pixel_size // 2) + i
                            y_pixel = y - (pixel_size // 2) + j
                            if (
                                0 <= x_pixel < display.width
                                and 0 <= y_pixel < display.height
                            ):
                                bitmap[x_pixel, y_pixel] = current_color
        except RuntimeError:
            pass
