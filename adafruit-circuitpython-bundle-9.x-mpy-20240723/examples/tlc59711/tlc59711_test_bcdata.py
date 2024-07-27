#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CircuitPython

# SPDX-FileCopyrightText: 2021 s-light
# SPDX-License-Identifier: MIT
# Author Stefan Krüger (s-light)

"""TLC5971 / TLC59711 Test BCData."""

__doc__ = """
tlc59711_test_bcdata.py.

test brightness correction data (BC)
"""

import time

import board
import busio
import supervisor

import adafruit_tlc59711

##########################################
PIXEL_COUNT = 16 * 8

spi = busio.SPI(board.SCK, MOSI=board.MOSI)
pixels = adafruit_tlc59711.TLC59711(spi, pixel_count=PIXEL_COUNT)

##########################################


def main_loop():
    """Loop."""
    new_value = input()
    if "v" in new_value:
        try:
            value = int(new_value[1:])
        except ValueError as e:
            print("Exception: ", e)
        pixels.set_pixel_all_16bit_value(value, value, value)
    else:
        Ioclmax, IoutR, IoutG, IoutB = (18, 18, 11, 13)
        try:
            Ioclmax, IoutR, IoutG, IoutB = new_value.split(";")
            Ioclmax = float(Ioclmax)
            IoutR = float(IoutR)
            IoutG = float(IoutG)
            IoutB = float(IoutB)
        except ValueError as e:
            print("Exception: ", e)
        BCValues = adafruit_tlc59711.TLC59711.calculate_BCData(
            Ioclmax=Ioclmax,
            IoutR=IoutR,
            IoutG=IoutG,
            IoutB=IoutB,
        )
        pixels.bcr = BCValues[0]
        pixels.bcg = BCValues[1]
        pixels.bcb = BCValues[2]
        print(
            "bcr: {:>3}\n"
            "bcg: {:>3}\n"
            "bcb: {:>3}\n"
            "".format(
                pixels.bcr,
                pixels.bcg,
                pixels.bcb,
            )
        )
        pixels.update_BCData()
    pixels.show()
    # prepare new input
    print("\nenter new values:")


def test_main():
    """Test Main."""
    print(42 * "*", end="")
    print(__doc__, end="")
    print(42 * "*")
    # print()
    # time.sleep(0.5)
    # print(42 * '*')

    print("set pixel all to 100, 100, 100")
    pixels.set_pixel_all((5000, 5000, 5000))
    # calculate bc values
    Ioclmax = adafruit_tlc59711.TLC59711.calculate_Ioclmax(Riref=2.7)
    print("Ioclmax = {}".format(Ioclmax))
    Riref = adafruit_tlc59711.TLC59711.calculate_Riref(Ioclmax=Ioclmax)
    print("Riref = {}".format(Riref))
    BCValues = adafruit_tlc59711.TLC59711.calculate_BCData(
        Ioclmax=Ioclmax,
        IoutR=18,
        IoutG=11,
        IoutB=13,
    )
    # (127, 77, 91)
    print("BCValues = {}".format(BCValues))
    pixels.bcr = BCValues[0]
    pixels.bcg = BCValues[1]
    pixels.bcb = BCValues[2]
    pixels.update_BCData()
    pixels.show()
    time.sleep(0.1)

    if supervisor.runtime.serial_connected:
        print(
            "\n"
            "this script offers two things to be changed:\n"
            "- value for all channels\n"
            "example: 'v10'\n"
            "example: 'v65535'\n"
            "- (global) brightness control:\n"
            "use format: 'Ioclmax; IoutR; IoutG; IoutB'\n"
            "example: '18; 7; 15; 17'"
            "\n"
        )
    while True:
        if supervisor.runtime.serial_bytes_available:
            main_loop()


##########################################
# main loop

if __name__ == "__main__":
    test_main()
