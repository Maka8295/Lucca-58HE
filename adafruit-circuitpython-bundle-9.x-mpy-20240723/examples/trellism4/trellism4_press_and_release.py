# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import adafruit_trellism4

trellis = adafruit_trellism4.TrellisM4Express()

current_press = set()
while True:
    pressed = set(trellis.pressed_keys)
    for press in pressed - current_press:
        print("Pressed:", press)
    for release in current_press - pressed:
        print("Released:", release)
    time.sleep(0.08)
    current_press = pressed
