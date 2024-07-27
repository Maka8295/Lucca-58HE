# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Simple test script for 5.6" 600x448 7-color ACeP display.
  """
# pylint: disable=no-member

import time
import board
import displayio
import adafruit_acep7in

# For 8.x.x and 9.x.x. When 8.x.x is discontinued as a stable release, change this.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire


displayio.release_displays()

# This pinout works on a Feather RP2040 and may need to be altered for other boards.
spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10
epd_reset = board.D11
epd_busy = board.D12

display_bus = FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)

display = adafruit_acep7in.ACeP7In(
    display_bus, width=800, height=480, busy_pin=epd_busy
)

g = displayio.Group()

fn = "/display-ruler-720p.bmp"

with open(fn, "rb") as f:
    pic = displayio.OnDiskBitmap(f)
    t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
    g.append(t)

    display.root_group = g

    display.refresh()

    time.sleep(120)
