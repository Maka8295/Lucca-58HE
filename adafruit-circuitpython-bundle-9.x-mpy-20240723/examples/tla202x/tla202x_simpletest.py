# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# pylint:disable=no-member
import board
import busio
from adafruit_tla202x import TLA2024

i2c = busio.I2C(board.SCL, board.SDA)
tla = TLA2024(i2c)

for i in range(4):
    channel = i
    tla.input_channel = channel
    print("Channel", channel, ":", tla.voltage)
