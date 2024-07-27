# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example uses the slide switch to control the little red LED. When the switch is to the
right it returns False, and when it's to the left, it returns True."""
from adafruit_circuitplayground import cp

while True:
    cp.red_led = cp.switch
