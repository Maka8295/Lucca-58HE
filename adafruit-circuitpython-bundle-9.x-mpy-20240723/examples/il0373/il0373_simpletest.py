# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test script for 2.13" 212x104 tri-color featherwing.

Supported products:
  * Adafruit 2.13" Tri-Color FeatherWing
    * https://www.adafruit.com/product/4128
  """

import time
import board
import displayio
import fourwire
import adafruit_il0373

displayio.release_displays()

epd_cs = board.D9
epd_dc = board.D10

display_bus = fourwire.FourWire(
    board.SPI(), command=epd_dc, chip_select=epd_cs, baudrate=1000000
)
time.sleep(1)

display = adafruit_il0373.IL0373(
    display_bus, width=212, height=104, rotation=90, highlight_color=0xFF0000
)

g = displayio.Group()

with open("/display-ruler.bmp", "rb") as f:
    pic = displayio.OnDiskBitmap(f)
    # CircuitPython 6 & 7 compatible
    t = displayio.TileGrid(
        pic, pixel_shader=getattr(pic, "pixel_shader", displayio.ColorConverter())
    )
    # CircuitPython 7 compatible only
    # t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
    g.append(t)

    display.root_group = g

    display.refresh()

    print("refreshed")

    time.sleep(120)
