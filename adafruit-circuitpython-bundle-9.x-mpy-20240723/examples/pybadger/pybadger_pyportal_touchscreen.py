# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simpletest example using Adafruit PyPortal. Uses the touchscreen to advance between examples."""
import board
import adafruit_touchscreen
from adafruit_pybadger import pybadger

# pylint: disable=invalid-name

# These pins are used as both analog and digital! XL, XR and YU must be analog
# and digital capable. YD just need to be digital
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(320, 240),
)

pybadger.show_badge(
    name_string="Blinka", hello_scale=2, my_name_is_scale=2, name_scale=3
)

cur_example = 0
prev_touch = None
while True:
    p = ts.touch_point
    if p and not prev_touch:
        cur_example += 1
        if cur_example >= 3:
            cur_example = 0
        print(cur_example)
    prev_touch = p

    if cur_example == 0:
        pybadger.show_business_card(
            image_name="Blinka_PyPortal.bmp",
            name_string="Blinka",
            name_scale=2,
            email_string_one="blinka@",
            email_string_two="adafruit.com",
        )
    elif cur_example == 1:
        pybadger.show_qr_code(data="https://circuitpython.org")
    elif cur_example == 2:
        pybadger.show_badge(
            name_string="Blinka", hello_scale=2, my_name_is_scale=2, name_scale=3
        )
