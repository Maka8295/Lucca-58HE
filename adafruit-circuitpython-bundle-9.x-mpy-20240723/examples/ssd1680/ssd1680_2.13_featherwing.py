# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: Unlicense


"""Simple test script for 2.13" 250x122 eInk Display FeatherWing
Supported products:
  * Adafruit 2.13" Tri-Color eInk Display FeatherWing
    * https://www.adafruit.com/product/4814
  * Adafruit 2.13" Mono eInk Display FeatherWing
    * https://www.adafruit.com/product/4195


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

    time.sleep(display.time_to_refresh + 5)
    # Always refresh a little longer. It's not a problem to refresh
    # a few seconds more, but it's terrible to refresh too early
    # (the display will throw an exception when if the refresh
    # is too soon)
    print("waited correct time")


# Keep the display the same
while True:
    time.sleep(10)
