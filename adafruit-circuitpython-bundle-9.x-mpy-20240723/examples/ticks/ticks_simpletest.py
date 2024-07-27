# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import board
import digitalio
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

# Turn an LED on or off every 100ms, so that it will blink at 5Hz.

deadline = ticks_ms()
while True:
    led.value = not led.value
    while ticks_less(ticks_ms(), deadline):
        pass
    deadline = ticks_add(deadline, 100)
