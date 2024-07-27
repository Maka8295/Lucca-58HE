# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example zeros the joystick, and prints when the joystick moves
   or the buttons are pressed."""
import time
from adafruit_featherwing import joy_featherwing

wing = joy_featherwing.JoyFeatherWing()
last_x = 0
last_y = 0

while True:
    x, y = wing.joystick
    if (abs(x - last_x) > 3) or (abs(y - last_y) > 3):
        last_x = x
        last_y = y
        print(x, y)
    if wing.button_a:
        print("Button A!")
    if wing.button_b:
        print("Button B!")
    if wing.button_x:
        print("Button X!")
    if wing.button_y:
        print("Button Y!")
    if wing.button_select:
        print("Button SELECT!")
    time.sleep(0.01)
