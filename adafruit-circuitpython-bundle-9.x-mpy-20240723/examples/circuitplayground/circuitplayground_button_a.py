# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example turns on the little red LED when button A is pressed."""
from adafruit_circuitplayground import cp

while True:
    if cp.button_a:
        print("Button A pressed!")
        cp.red_led = True
