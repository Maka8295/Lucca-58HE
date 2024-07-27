# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import storage
from adafruit_pyoa import PYOA_Graphics

try:
    try:
        import sdcardio

        sdcard = sdcardio.SDCard(board.SPI, board.SD_CS)
    except ImportError:
        import adafruit_sdcard
        import digitalio

        sdcard = adafruit_sdcard.SDCard(
            board.SPI(),
            digitalio.DigitalInOut(board.SD_CS),
        )
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    print("SD card found")  # no biggie
except OSError:
    print("No SD card found")  # no biggie

gfx = PYOA_Graphics()

gfx.load_game("/cyoa")
current_card = 0  # start with first card

while True:
    print("Current card:", current_card)
    current_card = gfx.display_card(current_card)
