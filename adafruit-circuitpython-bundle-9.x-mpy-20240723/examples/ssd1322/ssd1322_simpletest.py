# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import displayio
import adafruit_ssd1322

displayio.release_displays()

# This pinout works on a Metro and may need to be altered for other boards.
spi = busio.SPI(board.SCL, board.SDA)
tft_cs = board.D6
tft_dc = board.D9
tft_reset = board.D5

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset, baudrate=1000000
)
time.sleep(1)
display = adafruit_ssd1322.SSD1322(display_bus, width=256, height=64, colstart=28)
