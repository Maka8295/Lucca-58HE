# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example flashes the little red LED when the Circuit Playground is shaken."""
from adafruit_circuitplayground import cp

while True:
    if cp.shake(shake_threshold=20):
        print("Shake detected!")
        cp.red_led = True
    else:
        cp.red_led = False
