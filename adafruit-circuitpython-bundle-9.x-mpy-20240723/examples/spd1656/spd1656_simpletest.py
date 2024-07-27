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
import fourwire
import adafruit_spd1656


displayio.release_displays()

# This pinout works on a Feather RP2040 and may need to be altered for other boards.
spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10
epd_reset = board.D11
epd_busy = board.D12

display_bus = fourwire.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)

display = adafruit_spd1656.SPD1656(
    display_bus, width=600, height=448, busy_pin=epd_busy
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
