# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This is a hardware testing script for PBM
Tested with Feather M4 Express and 2.4" Featherwing
1. Flash board to 4x
2. add 'adafruit_ili9341.mpy' for 4x firmware to /lib/ on board
3. add /examples/images to /images on board
4. copy ./adafruit_imageload to /lib/ on the board
5. paste this file into code.py

"""

import board
import displayio
import adafruit_ili9341
import adafruit_imageload

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10

displayio.release_displays()
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)

display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

# Make the display context
splash = displayio.Group()
display.root_group = splash
# image = "images/netpbm_p1_mono_ascii.pbm"
# image = "images/netpbm_p2_ascii.pgm"
# image = "images/netpbm_p3_rgb_ascii.ppm"
# image = "images/netpbm_p4_mono_binary.pbm"
# image = "images/netpbm_p5_binary.pgm"
image = "images/netpbm_p6_binary.ppm"

bitmap, palette = adafruit_imageload.load(
    image, bitmap=displayio.Bitmap, palette=displayio.Palette
)


bg_sprite = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)
splash.append(bg_sprite)

while True:
    pass
