# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test script for 4.2" 400x300 tri-color displays.

Supported products:
  * WaveShare 4.2" Color
    * https://www.waveshare.com/product/modules/oleds-lcds/e-paper/4.2inch-e-paper-b.htm
    * https://www.waveshare.com/product/modules/oleds-lcds/e-paper/4.2inch-e-paper-c.htm
    * https://www.waveshare.com/product/modules/oleds-lcds/e-paper/4.2inch-e-paper-module-c.htm
    * https://www.waveshare.com/product/modules/oleds-lcds/e-paper/4.2inch-e-paper-module-b.htm
  """

import time
import board
import displayio
import adafruit_il0398

# Compatibility with both CircuitPython 8.x.x and 9.x.x.
# Remove after 8.x.x is no longer a supported release.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

displayio.release_displays()

# This pinout works on a Feather M4 and may need to be altered for other boards.
spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10
epd_reset = board.D5
epd_busy = board.D6

display_bus = FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)
time.sleep(1)

display = adafruit_il0398.IL0398(
    display_bus,
    width=400,
    height=300,
    seconds_per_frame=20,
    highlight_color=0xFF0000,
    busy_pin=epd_busy,
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

    time.sleep(120)
