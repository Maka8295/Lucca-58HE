# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example shows how you can use single-tap and double-tap together with a delay between.
Single-tap the board twice and then double-tap the board twice to complete the program."""
from adafruit_circuitplayground import cp

# Set to check for single-taps.
cp.detect_taps = 1
tap_count = 0

# We're looking for 2 single-taps before moving on.
while tap_count < 2:
    if cp.tapped:
        tap_count += 1
print("Reached 2 single-taps!")

# Now switch to checking for double-taps
tap_count = 0
cp.detect_taps = 2

# We're looking for 2 double-taps before moving on.
while tap_count < 2:
    if cp.tapped:
        tap_count += 1
print("Reached 2 double-taps!")
print("Done.")
while True:
    cp.red_led = True
