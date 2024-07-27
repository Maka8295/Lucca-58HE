# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example uses the light sensor on your Circuit Playground, located next to the picture of
the eye. Try shining a flashlight on your Circuit Playground, or covering the light sensor with
your finger to see the values increase and decrease."""
import time
from adafruit_circuitplayground import cp

while True:
    print("Light:", cp.light)
    time.sleep(0.2)
