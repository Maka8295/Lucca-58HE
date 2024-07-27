# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example uses the slide switch to control the little red LED."""
from adafruit_circuitplayground import cp

# This code is written to be readable versus being Pylint compliant.
# pylint: disable=simplifiable-if-statement

while True:
    if cp.switch:
        cp.red_led = True
    else:
        cp.red_led = False
