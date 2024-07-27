# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import digitalio
import busio
import board
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1680 import Adafruit_SSD1680

# create the spi device and pins we will need
spi = busio.SPI(board.EPD_SCK, MOSI=board.EPD_MOSI, MISO=None)
epd_cs = digitalio.DigitalInOut(board.EPD_CS)
epd_dc = digitalio.DigitalInOut(board.EPD_DC)
epd_reset = digitalio.DigitalInOut(board.EPD_RESET)
epd_busy = digitalio.DigitalInOut(board.EPD_BUSY)
srcs = None

display = Adafruit_SSD1680(
    122,
    250,
    spi,
    cs_pin=epd_cs,
    dc_pin=epd_dc,
    sramcs_pin=srcs,
    rst_pin=epd_reset,
    busy_pin=epd_busy,
)

display.rotation = 3
display.fill(Adafruit_EPD.WHITE)

display.fill_rect(20, 20, 50, 60, Adafruit_EPD.BLACK)
display.hline(80, 30, 60, Adafruit_EPD.BLACK)
display.vline(80, 30, 60, Adafruit_EPD.BLACK)

# draw repeatedly with pauses
while True:
    display.display()
    time.sleep(15)
