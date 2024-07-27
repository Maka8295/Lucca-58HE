# SPDX-FileCopyrightText: 2023 DJDevon3
# SPDX-License-Identifier: MIT
""" Screenshot on a 3.5" TFT Featherwing (integrated SD Card) """
# pylint:disable=invalid-name

import board
import digitalio
import displayio
import adafruit_sdcard
import storage
from adafruit_hx8357 import HX8357
from adafruit_bitmapsaver import save_pixels

displayio.release_displays()

# 3.5" TFT Featherwing is 480x320 pixels
DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320

TAKE_SCREENSHOT = False  # Set to True to take a screenshot

# Initialize SPI Bus
spi = board.SPI()

# Initialize TFT Featherwing Display
tft_cs = board.D9
tft_dc = board.D10
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = HX8357(display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)

if TAKE_SCREENSHOT:
    # Initialize SD Card & Mount Virtual File System
    cs = digitalio.DigitalInOut(board.D5)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    virtual_root = "/sd"  # /sd is root dir of SD Card
    storage.mount(vfs, virtual_root)

    print("Taking Screenshot... ")
    save_pixels("/sd/screenshot.bmp", display)
    print("Screenshot Saved")
    storage.umount(vfs)
    print("SD Card Unmounted")  # Do not remove SD card until unmounted
