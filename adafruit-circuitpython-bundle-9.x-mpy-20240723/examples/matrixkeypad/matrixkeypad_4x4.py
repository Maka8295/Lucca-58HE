# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from digitalio import DigitalInOut
import board
import adafruit_matrixkeypad

# Extended 4x4 matrix keypad
cols = [DigitalInOut(x) for x in (board.D0, board.D1, board.D2, board.D3)]
rows = [DigitalInOut(x) for x in (board.D4, board.D5, board.D6, board.D7)]
keys = ((1, 2, 3, "A"), (4, 5, 6, "B"), (7, 8, 9, "C"), ("*", 0, "#", "D"))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

while True:
    keys = keypad.pressed_keys
    if keys:
        print("Pressed: ", keys)
    time.sleep(0.1)
