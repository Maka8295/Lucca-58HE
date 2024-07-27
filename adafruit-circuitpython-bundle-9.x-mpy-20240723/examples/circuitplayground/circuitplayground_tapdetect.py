# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example prints to the serial console when the board is double-tapped."""
import time
from adafruit_circuitplayground import cp

# Change to 1 for single-tap detection.
cp.detect_taps = 2

while True:
    if cp.tapped:
        print("Tapped!")
    time.sleep(0.05)
