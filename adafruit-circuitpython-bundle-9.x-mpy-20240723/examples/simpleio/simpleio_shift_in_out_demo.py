# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
'shift_in_out_demo.py'.

=================================================
shifts data into and out of a data pin
"""

import time
import board
import digitalio
import simpleio

# set up clock, data, and latch pins
clk = digitalio.DigitalInOut(board.D12)
data = digitalio.DigitalInOut(board.D11)
latch = digitalio.DigitalInOut(board.D10)
clk.direction = digitalio.Direction.OUTPUT
latch.direction = digitalio.Direction.OUTPUT

while True:
    data_to_send = 256
    # shifting 256 bits out of data pin
    latch.value = False
    data.direction = digitalio.Direction.OUTPUT
    print("shifting out...")
    simpleio.shift_out(data, clk, data_to_send, msb_first=False)
    latch.value = True
    time.sleep(3)

    # shifting 256 bits into the data pin
    latch.value = False
    data.direction = digitalio.Direction.INPUT
    print("shifting in...")
    simpleio.shift_in(data, clk)
    time.sleep(3)
