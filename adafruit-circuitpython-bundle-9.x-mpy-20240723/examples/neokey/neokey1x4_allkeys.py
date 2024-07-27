# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""NeoKey simpletest."""
from time import sleep
import board
from adafruit_neokey.neokey1x4 import NeoKey1x4

# use default I2C bus
i2c_bus = board.I2C()

# Create a NeoKey object
neokey = NeoKey1x4(i2c_bus, addr=0x30)

print("Adafruit NeoKey simple test reading all keys")

# neokey.edbug = True

while True:
    keys = neokey.get_keys()
    print(f"keys {keys}")
    # test for all buttons pressed at once
    if keys[0] and keys[1] and keys[2] and keys[3]:
        for i in range(4):
            neokey.pixels[i] = 0xFF00FF
    # check each key individually
    else:
        if keys[0]:
            print("Button A")
            neokey.pixels[0] = 0xFF0000
        else:
            neokey.pixels[0] = 0x0

        if keys[1]:
            print("Button B")
            neokey.pixels[1] = 0xFFFF00
        else:
            neokey.pixels[1] = 0x0

        if keys[2]:
            print("Button C")
            neokey.pixels[2] = 0x00FF00
        else:
            neokey.pixels[2] = 0x0

        if keys[3]:
            print("Button D")
            neokey.pixels[3] = 0x00FFFF
        else:
            neokey.pixels[3] = 0x0

    sleep(0.5)
