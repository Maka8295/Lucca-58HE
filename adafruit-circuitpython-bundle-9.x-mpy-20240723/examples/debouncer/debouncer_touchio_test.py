# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example shows how to use the debouncer library on the signals coming from
a cap-sense pin with touchio.
"""
import time
import board
import touchio
from adafruit_debouncer import Debouncer

touch_pad = board.A1
touch = touchio.TouchIn(touch_pad)
touch_debounced = Debouncer(touch)

while True:
    touch_debounced.update()
    if touch_debounced.fell:
        print("Just released")
    if touch_debounced.rose:
        print("Just pressed")
    if touch_debounced.value:
        print("touching")
    else:
        # print('not touching')
        pass
    time.sleep(0.05)
