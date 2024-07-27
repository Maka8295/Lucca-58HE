#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CircuitPython

# SPDX-FileCopyrightText: 2021 s-light
# SPDX-License-Identifier: MIT
# Author Stefan Krüger (s-light)

"""TLC5971 / TLC59711 Example."""

__doc__ = """
tlc59711_fastset.py - TLC59711 fast set example.

showcases the usage of set_pixel_16bit_value for fastest setting of values.
for speed comparision of all the available set calls
look at the tlc59711_dev.py file.

Enjoy the colors :-)
"""


import time

import board
import busio

import adafruit_tlc59711


##########################################
PIXEL_COUNT = 16

spi = busio.SPI(board.SCK, MOSI=board.MOSI)
pixels = adafruit_tlc59711.TLC59711(spi, pixel_count=PIXEL_COUNT)


##########################################
# test function


def channelcheck_update_pixel(offset):
    """Channel check pixel."""
    # print("offset", offset)

    pixels.set_pixel_16bit_value(offset, 1000, 100, 0)
    # clear last pixel
    last = offset - 1
    if last < 0:
        last = PIXEL_COUNT - 1
    pixels.set_pixel_16bit_value(last, 0, 0, 1)
    pixels.show()

    offset += 1
    if offset >= PIXEL_COUNT:
        time.sleep(0.2)
        offset = 0
        print("clear")
        pixels.set_pixel_all_16bit_value(0, 1, 0)
        pixels.show()
    return offset


def test_main():
    """Test Main."""
    print(42 * "*", end="")
    print(__doc__, end="")
    print(42 * "*")

    bcvalues = adafruit_tlc59711.TLC59711.calculate_BCData(
        Ioclmax=18,
        IoutR=18,
        IoutG=11,
        IoutB=13,
    )
    print("bcvalues = {}".format(bcvalues))
    pixels.bcr = bcvalues[0]
    pixels.bcg = bcvalues[1]
    pixels.bcb = bcvalues[2]
    pixels.update_BCData()
    pixels.show()

    offset = 0

    print("loop:")
    while True:
        offset = channelcheck_update_pixel(offset)
        time.sleep(0.2)


##########################################
# main loop

if __name__ == "__main__":
    test_main()
