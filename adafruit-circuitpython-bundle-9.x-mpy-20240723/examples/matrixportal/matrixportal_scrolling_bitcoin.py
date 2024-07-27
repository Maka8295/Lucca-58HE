# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
This example checks the current Bitcoin price and scrolls it across the screen
"""
import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

# You can display in 'GBP', 'EUR' or 'USD'
CURRENCY = "USD"
# Set up where we'll be fetching data from
DATA_SOURCE = "https://api.coindesk.com/v1/bpi/currentprice.json"
DATA_LOCATION = ["bpi", CURRENCY, "rate_float"]


def text_transform(val):
    if CURRENCY == "USD":
        return "$%d" % val
    if CURRENCY == "EUR":
        return "‎€%d" % val
    if CURRENCY == "GBP":
        return "£%d" % val
    return "%d" % val


# the current working directory (where this file is)
cwd = ("/" + __file__).rsplit("/", 1)[0]

matrixportal = MatrixPortal(
    url=DATA_SOURCE,
    json_path=DATA_LOCATION,
    status_neopixel=board.NEOPIXEL,
)

matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(16, 16),
    text_color=0xFFFFFF,
    text_transform=text_transform,
    scrolling=True,
)
matrixportal.preload_font(b"$012345789")  # preload numbers
matrixportal.preload_font((0x00A3, 0x20AC))  # preload gbp/euro symbol

last_check = None

while True:
    if last_check is None or time.monotonic() > last_check + 180:
        try:
            value = matrixportal.fetch()
            print("Response is", value)
            last_check = time.monotonic()
        except (ValueError, RuntimeError) as e:
            print("Some error occured, retrying! -", e)
    matrixportal.scroll()
    time.sleep(0.03)
