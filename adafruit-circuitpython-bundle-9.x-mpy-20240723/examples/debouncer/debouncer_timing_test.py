# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer

button = DigitalInOut(board.D4)
button.direction = Direction.INPUT
button.pull = Pull.UP
switch = Debouncer(button)

while True:
    switch.update()
    if switch.fell:
        print("pressed")
        print("was released for ", switch.last_duration)
    elif switch.rose:
        print("released")
        print("was pressed for ", switch.last_duration)
    else:
        print("Stable for ", switch.current_duration)
    time.sleep(0.1)
