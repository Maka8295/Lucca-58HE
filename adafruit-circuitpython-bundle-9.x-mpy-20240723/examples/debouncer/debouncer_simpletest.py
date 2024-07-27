# SPDX-FileCopyrightText: 2019 Dave Astels for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=invalid-name

import board
import digitalio
from adafruit_debouncer import Debouncer

pin = digitalio.DigitalInOut(board.D12)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
switch = Debouncer(pin)

while True:
    switch.update()
    if switch.fell:
        print("Just pressed")
    if switch.rose:
        print("Just released")
    if switch.value:
        print("not pressed")
    else:
        print("pressed")
