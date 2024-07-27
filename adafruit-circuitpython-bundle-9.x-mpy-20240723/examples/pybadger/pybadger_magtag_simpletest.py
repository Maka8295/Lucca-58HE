# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simpletest example using the Mag Tag.
   Use the A, B, and C buttons to change between examples."""
import time
import board
import digitalio
from adafruit_pybadger import pybadger


def try_refresh():
    """Attempt to refresh the display. Catch 'refresh too soon' error
    and retry after waiting 10 seconds.
    """
    try:
        board.DISPLAY.refresh()
    except RuntimeError as too_soon_error:
        # catch refresh too soon
        print(too_soon_error)
        print("waiting before retry refresh()")
        time.sleep(10)
        board.DISPLAY.refresh()


print("wait before anything")
time.sleep(5)

btn_a = digitalio.DigitalInOut(board.BUTTON_A)
btn_a.direction = digitalio.Direction.INPUT
btn_a.pull = digitalio.Pull.UP

btn_b = digitalio.DigitalInOut(board.BUTTON_B)
btn_b.direction = digitalio.Direction.INPUT
btn_b.pull = digitalio.Pull.UP

btn_c = digitalio.DigitalInOut(board.BUTTON_C)
btn_c.direction = digitalio.Direction.INPUT
btn_c.pull = digitalio.Pull.UP

prev_a = btn_a.value
prev_b = btn_b.value
prev_c = btn_c.value

SHOWING = "badge"

pybadger.show_badge(
    name_string="Blinka", hello_scale=2, my_name_is_scale=2, name_scale=3
)

try_refresh()

print("after show, going to loop")

pybadger.pixels.fill(0x000022)

while True:
    cur_a = btn_a.value
    cur_b = btn_b.value
    cur_c = btn_c.value

    if prev_a and not cur_a:
        pybadger.pixels.fill(0x000000)
        if SHOWING != "badge":
            print("changing to badge")
            SHOWING = "badge"
            pybadger.show_badge(
                name_string="Mag Tag", hello_scale=2, my_name_is_scale=2, name_scale=3
            )
            try_refresh()

    if prev_b and not cur_b:
        pybadger.pixels.fill(0x000000)
        if SHOWING != "qr":
            print("changing to qr")
            SHOWING = "qr"
            pybadger.show_qr_code(data="https://www.adafruit.com/product/4800")
            try_refresh()

    if prev_c and not cur_c:
        pybadger.pixels.fill(0x000000)
        if SHOWING != "card":
            print("changing to card")
            SHOWING = "card"
            pybadger.show_business_card(
                image_name="Blinka_MagTag.bmp",
                name_string="Blinka",
                name_scale=2,
                email_string_one="blinka@",
                email_string_two="adafruit.com",
            )
            # show_business_card() calls refresh() internally

    prev_a = cur_a
    prev_b = cur_b
    prev_c = cur_c
    time.sleep(1)
