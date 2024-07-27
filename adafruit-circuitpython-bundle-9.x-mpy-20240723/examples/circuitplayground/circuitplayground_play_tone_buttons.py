# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example plays a different tone for a duration of 1 second for each button pressed."""
from adafruit_circuitplayground import cp

while True:
    if cp.button_a:
        cp.play_tone(262, 1)
    if cp.button_b:
        cp.play_tone(294, 1)
