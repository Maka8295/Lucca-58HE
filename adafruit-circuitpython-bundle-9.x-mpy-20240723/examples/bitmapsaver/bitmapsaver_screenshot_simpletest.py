# SPDX-FileCopyrightText: 2019 Dave Astels for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Example of taking a screenshot."""

# pylint:disable=invalid-name
import board
import digitalio
import busio
import adafruit_sdcard
import storage
from adafruit_bitmapsaver import save_pixels

TAKE_SCREENSHOT = False  # Set to True to take a screenshot

if TAKE_SCREENSHOT:
    # Initialize SD Card & Mount Virtual File System
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.SD_CS)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")  # /sd is root dir of SD Card

    print("Taking Screenshot... ")
    save_pixels("/sd/screenshot.bmp")
    print("Screenshot Saved")
    storage.umount(vfs)
    print("SD Card Unmounted")  # Do not remove SD card until unmounted
