# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""Example for connecting two NeoKey 1x4 breakouts. Requires bridging the A0 jumper on one board."""
import board
from rainbowio import colorwheel
from adafruit_neokey.neokey1x4 import NeoKey1x4

# Create a NeoKey object
neokey1 = NeoKey1x4(board.I2C())
neokey2 = NeoKey1x4(board.I2C(), addr=0x31)

keys = [
    (neokey1, 0, colorwheel(0)),
    (neokey1, 1, colorwheel(32)),
    (neokey1, 2, colorwheel(64)),
    (neokey1, 3, colorwheel(96)),
    (neokey2, 0, colorwheel(128)),
    (neokey2, 1, colorwheel(160)),
    (neokey2, 2, colorwheel(192)),
    (neokey2, 3, colorwheel(224)),
]

off = (0, 0, 0)

# Check each button, if pressed, light up the matching NeoPixel!
while True:
    for i in range(8):
        neokey, key_number, color = keys[i]
        if neokey[key_number]:
            print("Button", i)
            neokey.pixels[key_number] = color
        else:
            neokey.pixels[key_number] = off
