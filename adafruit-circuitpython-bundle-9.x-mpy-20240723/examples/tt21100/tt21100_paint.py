# SPDX-FileCopyrightText: 2022 Scott Shawcroft for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Simple painting demo that draws on the ESP32-S3 Box display in red for the first
touch and blue for the second concurrent touch.
"""

import bitmaptools
import busio
import board
import displayio
import adafruit_tt21100

# Create library object using our Bus I2C & SPI port
i2c = busio.I2C(board.SCL, board.SDA)
tt = adafruit_tt21100.TT21100(i2c)

# Setup a full screen bitmap that we'll modify based on touches
display = board.DISPLAY
pixels = displayio.Bitmap(display.width, display.height, 4)
palette = displayio.Palette(4)
palette[1] = 0xFF0000
palette[2] = 0x0000FF
tg = displayio.TileGrid(pixels, pixel_shader=palette)
g = displayio.Group()
g.append(tg)
display.root_group = g

while True:
    for point in tt.touches:
        # perform transformation to get into display coordinate system!
        y = point["y"]
        x = display.width - point["x"]
        size = point["pressure"] - 20
        bitmaptools.fill_region(
            pixels, x - size, y - size, x + size, y + size, point["id"] + 1
        )
