# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# pylint:disable=no-member
"""
≥ +FS (2^11 – 1) / 2^11  ==>  0x7FF0
+FS /2^11                ==>  0x0010
0                        ==>  0x0000
-FS /2^11                ==>  0xFFF0
≤ –FS                    ==>  0x8000
"""
import board
import busio
from adafruit_tla202x import TLA2024

i2c = busio.I2C(board.SCL, board.SDA)
tla = TLA2024(i2c)
