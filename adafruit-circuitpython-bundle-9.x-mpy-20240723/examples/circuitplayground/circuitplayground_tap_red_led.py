# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example turns on the little red LED and prints to the serial console when you double-tap
the Circuit Playground!"""
import time
from adafruit_circuitplayground import cp

# Change to 1 for detecting a single-tap!
cp.detect_taps = 2

while True:
    if cp.tapped:
        print("Tapped!")
        cp.red_led = True
        time.sleep(0.1)
    else:
        cp.red_led = False
