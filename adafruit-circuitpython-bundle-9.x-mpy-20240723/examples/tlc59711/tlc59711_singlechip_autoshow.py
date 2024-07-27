#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CircuitPython

# SPDX-FileCopyrightText: 2021 s-light
# SPDX-License-Identifier: MIT
# Author Stefan Krüger (s-light)

"""TLC5971 / TLC59711 Example."""

__doc__ = """
tlc59711_singlechip_autoshow.py - TLC59711AutoShow minimal usage example.

simple demo of the TLC59711 16-bit 12 channel LED PWM driver.
Shows the minimal usage - how to set pixel values.
the TLC59711AutoShow class automatically writes the pixel values on each change.
this makes it very slow on lots of pixel changs but is convenient for only a handfull of pixels..

Author: Tony DiCola, Stefan Krueger

Enjoy the colors :-)
"""

import board
import busio

import adafruit_tlc59711

print(__doc__)

# Define SPI bus connected to chip.
# You only need the clock and MOSI (output) line to use this chip.
spi = busio.SPI(board.SCK, MOSI=board.MOSI)
pixels = adafruit_tlc59711.TLC59711AutoShow(spi)

# Ways to set the values:
# just a list or tuple with 3 integer values: R G B
# each 0 - 65535 or 0.0 - 1.0
# every chip has 4 RGB-LEDs (=12 Channel)
pixels[0] = (100, 100, 10111)
pixels[1] = (0, 0, 100)
pixels[2] = (0.01, 0.0, 0.01)
pixels[3] = (0.1, 0.01, 0.0)

# You can also explicitly control each R0, G0, B0, R1, B1, etc. channel of the first ic
# by getting and setting its 16-bit value directly with properties.
# For example set channel 2 to 1/4 green (i.e. G2):
pixels.g2 = 65535 // 4

# there are a bunch of other advanced ways to set pixel.
# have a look at the other examples.
