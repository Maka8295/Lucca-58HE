# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Test your Trellis M4 Express without needing the serial output.
Press any button and the rest will light up the same color!"""
import time
from rainbowio import colorwheel
import adafruit_trellism4

trellis = adafruit_trellism4.TrellisM4Express()

for x in range(trellis.pixels.width):
    for y in range(trellis.pixels.height):
        pixel_index = ((y * 8) + x) * 256 // 32
        trellis.pixels[x, y] = colorwheel(pixel_index & 255)


current_press = set()
while True:
    pressed = set(trellis.pressed_keys)
    for press in pressed - current_press:
        if press:
            print("Pressed:", press)
            pixel = (press[1] * 8) + press[0]
            pixel_index = pixel * 256 // 32
            trellis.pixels.fill(colorwheel(pixel_index & 255))
    for release in current_press - pressed:
        if release:
            print("Released:", release)
            for x in range(trellis.pixels.width):
                for y in range(trellis.pixels.height):
                    pixel_index = ((y * 8) + x) * 256 // 32
                    trellis.pixels[x, y] = colorwheel(pixel_index & 255)
    time.sleep(0.08)
    current_press = pressed
