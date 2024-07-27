# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from adafruit_debouncer import Debouncer
from adafruit_pybadger import pybadger

b_btn = Debouncer(lambda: pybadger.button.b == 0)
a_btn = Debouncer(lambda: pybadger.button.a == 0)
up_btn = Debouncer(lambda: pybadger.button.up == 0)
down_btn = Debouncer(lambda: pybadger.button.down == 0)
left_btn = Debouncer(lambda: pybadger.button.left == 0)
right_btn = Debouncer(lambda: pybadger.button.right == 0)

while True:
    b_btn.update()
    a_btn.update()
    up_btn.update()
    down_btn.update()
    right_btn.update()
    left_btn.update()

    if b_btn.fell:
        print("B pressed")
    if b_btn.rose:
        print("B released")

    if a_btn.fell:
        print("A pressed")
    if a_btn.rose:
        print("A released")

    if up_btn.fell:
        print("UP pressed")
    if up_btn.rose:
        print("UP released")

    if down_btn.fell:
        print("DOWN pressed")
    if down_btn.rose:
        print("DOWN released")

    if right_btn.fell:
        print("RIGHT pressed")
    if right_btn.rose:
        print("RIGHT released")

    if left_btn.fell:
        print("LEFT pressed")
    if left_btn.rose:
        print("LEFT released")
