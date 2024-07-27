# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example turns the little red LED on only while button B is currently being pressed."""
from adafruit_circuitplayground import cp

# This code is written to be readable versus being Pylint compliant.
# pylint: disable=simplifiable-if-statement

while True:
    if cp.button_b:
        cp.red_led = True
    else:
        cp.red_led = False

# Can also be written as:
#    cp.red_led = cp.button_b
