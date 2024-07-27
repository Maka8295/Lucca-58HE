# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simpletest example using the Pew Pew M4.
   Use the O, X, and Z buttons to change between examples."""
from adafruit_pybadger import pybadger

pybadger.show_badge(
    name_string="Blinka", hello_scale=3, my_name_is_scale=3, name_scale=4
)

while True:
    if pybadger.button.o:
        pybadger.show_business_card(
            image_name="Blinka_PewPewM4.bmp",
            name_string="Blinka",
            name_scale=4,
            email_string_one="blinka@",
            email_string_two="adafruit.com",
            email_scale_one=2,
            email_scale_two=2,
        )
    elif pybadger.button.x:
        pybadger.show_qr_code(data="https://circuitpython.org")
    elif pybadger.button.z:
        pybadger.show_badge(
            name_string="Blinka", hello_scale=3, my_name_is_scale=3, name_scale=4
        )
