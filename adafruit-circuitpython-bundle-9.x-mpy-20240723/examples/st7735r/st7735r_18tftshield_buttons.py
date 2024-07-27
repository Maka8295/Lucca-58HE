# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example will test out the display on the 1.8" TFT Shield
"""
import time
import board
import displayio
from adafruit_seesaw.tftshield18 import TFTShield18
from adafruit_st7735r import ST7735R

# Support both 8.x.x and 9.x.x. Change when 8.x.x is discontinued as a stable release.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

# Release any resources currently in use for the displays
displayio.release_displays()

ss = TFTShield18()

spi = board.SPI()
tft_cs = board.D10
tft_dc = board.D8

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)

ss.tft_reset()
display = ST7735R(display_bus, width=160, height=128, rotation=90, bgr=True)

ss.set_backlight(True)

while True:
    buttons = ss.buttons

    if buttons.right:
        print("Button RIGHT!")

    if buttons.down:
        print("Button DOWN!")

    if buttons.left:
        print("Button LEFT!")

    if buttons.up:
        print("Button UP!")

    if buttons.select:
        print("Button SELECT!")

    if buttons.a:
        print("Button A!")

    if buttons.b:
        print("Button B!")

    if buttons.c:
        print("Button C!")

    time.sleep(0.001)
