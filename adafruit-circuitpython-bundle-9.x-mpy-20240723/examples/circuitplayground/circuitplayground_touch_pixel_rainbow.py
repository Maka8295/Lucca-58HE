# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example uses the capacitive touch pads on the Circuit Playground. They are located around
the outer edge of the board and are labeled A1-A6 and TX. (A0 is not a touch pad.) This example
lights up the nearest NeoPixel to that pad a different color of the rainbow!"""
import time
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.3

while True:
    if cp.touch_A1:
        print("Touched A1!")
        cp.pixels[6] = (255, 0, 0)
    if cp.touch_A2:
        print("Touched A2!")
        cp.pixels[8] = (210, 45, 0)
    if cp.touch_A3:
        print("Touched A3!")
        cp.pixels[9] = (155, 100, 0)
    if cp.touch_A4:
        print("Touched A4!")
        cp.pixels[0] = (0, 255, 0)
    if cp.touch_A5:
        print("Touched A5!")
        cp.pixels[1] = (0, 135, 125)
    if cp.touch_A6:
        print("Touched A6!")
        cp.pixels[3] = (0, 0, 255)
    if cp.touch_TX:
        print("Touched TX!")
        cp.pixels[4] = (100, 0, 155)
    time.sleep(0.1)
