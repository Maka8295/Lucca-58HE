# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense


import board
import adafruit_cst8xx

ctp = adafruit_cst8xx.Adafruit_CST8XX(board.I2C())

events = adafruit_cst8xx.EVENTS
while True:
    if ctp.touched:
        for touch_id, touch in enumerate(ctp.touches):
            x = touch["x"]
            y = touch["y"]
            event = events[touch["event_id"]]
            print(f"touch_id: {touch_id}, x: {x}, y: {y}, event: {event}")
