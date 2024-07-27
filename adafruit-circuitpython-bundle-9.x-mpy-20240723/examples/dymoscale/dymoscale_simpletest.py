# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import adafruit_dymoscale

# initialize the dymo scale
units_pin = digitalio.DigitalInOut(board.D3)
units_pin.switch_to_output()
dymo = adafruit_dymoscale.DYMOScale(board.D4, units_pin)

# take a reading of the current time
time_stamp = time.monotonic()

while True:
    reading = dymo.weight
    text = "{} g".format(reading.weight)
    print(text)
    # to avoid sleep mode, toggle the units pin every 2 mins.
    if (time.monotonic() - time_stamp) > 120:
        print("toggling units button...")
        dymo.toggle_unit_button()
        # reset the time
        time_stamp = time.monotonic()
