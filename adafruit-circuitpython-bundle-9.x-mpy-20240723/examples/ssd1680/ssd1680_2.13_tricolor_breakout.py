# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: Unlicense


"""Simple test script for Adafruit 2.13" Tri-Color eInk Display Breakout
Supported products:
  * Adafruit 2.13" Tri-Color eInk Display Breakout
    * https://www.adafruit.com/product/4947

"""

import time
import board
import displayio
import adafruit_ssd1680

# For 8.x.x and 9.x.x. When 8.x.x is discontinued as a stable release, change this.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

displayio.release_displays()

# This pinout works on a Metro M4 and may need to be altered for other boards.
spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10
epd_reset = board.D5
epd_busy = board.D6

display_bus = FourWire(spi, command=epd_dc, chip_select=epd_cs, baudrate=1000000)
time.sleep(1)

display = adafruit_ssd1680.SSD1680(
    display_bus,
    width=250,
    height=122,
    highlight_color=0xFF0000,
    rotation=270,
)

g = displayio.Group()

with open("/display-ruler.bmp", "rb") as f:
    pic = displayio.OnDiskBitmap(f)

    t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)

    g.append(t)

    display.root_group = g

    display.refresh()

    print("refreshed")

    time.sleep(120)
