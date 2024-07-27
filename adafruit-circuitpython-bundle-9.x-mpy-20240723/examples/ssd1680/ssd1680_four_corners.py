# SPDX-FileCopyrightText: Copyright (c) 2023 Scott Shawcroft for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Test partial updates by moving a simple label around each of the four corners."""

# The top left is 0 or 4, top right is 1 or 5, bottom left is 2 or 6 and bottom
# right is 3 or 7. (It does % 8 for the label and % 4 for position.)
# pylint: disable=no-member

import time
import board
import busio
import displayio
import terminalio
import adafruit_ssd1680

# For 8.x.x and 9.x.x. When 8.x.x is discontinued as a stable release, change this.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

displayio.release_displays()

# This pinout works on a Feather RP2040 EPD and may need to be altered for other
# boards. The newer SSD1680 version with FPC on the ribbon cable 2.13" dual color
# is connected directly via the ribbon cable.
spi = busio.SPI(board.EPD_SCK, board.EPD_MOSI)  # Uses SCK and MOSI
epd_cs = board.EPD_CS
epd_dc = board.EPD_DC
epd_reset = board.EPD_RESET
epd_busy = board.EPD_BUSY

display_bus = FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)
display = adafruit_ssd1680.SSD1680(
    display_bus,
    width=250,
    height=122,
    busy_pin=epd_busy,
    highlight_color=0xFFFFFF,
    rotation=270,
    seconds_per_frame=10,
)

# Make the display context
main_group = displayio.Group()
display.root_group = main_group

palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xFFFFFF

zero_glyph = terminalio.FONT.get_glyph(ord("0"))

padding = max(zero_glyph.height, zero_glyph.width) + 1
label = displayio.TileGrid(
    terminalio.FONT.bitmap,
    pixel_shader=palette,
    tile_width=zero_glyph.width,
    tile_height=zero_glyph.height,
)
main_group.append(label)

# Number each of the 4 corners
i = 0
while True:
    if i % 2 == 0:
        label.x = padding
    else:
        label.x = display.width - padding - zero_glyph.width
    if (i % 4) // 2 == 0:
        label.y = padding
    else:
        label.y = display.height - padding - zero_glyph.height

    label[0] = zero_glyph.tile_index + i

    # update text property to change the text showing on the display
    sleep_time = display.time_to_refresh
    print(f"Sleeping {sleep_time} seconds")
    time.sleep(sleep_time)

    print(f"{i % 8} @ ({label.x}, {label.y})")
    display.refresh()

    i += 1
    i %= 8
