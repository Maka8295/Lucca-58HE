# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from rainbowio import colorwheel
import adafruit_trellism4

trellis = adafruit_trellism4.TrellisM4Express()

led_on = []

for x in range(trellis.pixels.width):
    led_on.append([])
    for y in range(trellis.pixels.height):
        led_on[x].append(False)

trellis.pixels.fill((0, 0, 0))

current_press = set()

while True:
    pressed = set(trellis.pressed_keys)

    for press in pressed - current_press:
        x, y = press

        if not led_on[x][y]:
            print("Turning on:", press)
            pixel_index = (x + (y * 8)) * 256 // 32
            trellis.pixels[x, y] = colorwheel(pixel_index & 255)
            led_on[x][y] = True

        else:
            print("Turning off:", press)
            trellis.pixels[x, y] = (0, 0, 0)
            led_on[x][y] = False

    current_press = pressed
