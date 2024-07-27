# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example will display a CircuitPython console and
print the coordinates of touchscreen presses.

It will also try to write and then read a file on the
SD Card.
"""
from adafruit_featherwing import tft_featherwing_35

tft_featherwing = tft_featherwing_35.TFTFeatherWing35()

try:
    with open("/sd/tft_featherwing.txt", "w") as f:
        f.write("Blinka\nBlackberry Q10 Keyboard")

    with open("/sd/tft_featherwing.txt", "r") as f:
        print(f.read())
except OSError as error:
    print("Unable to write to SD Card.")


while True:
    if not tft_featherwing.touchscreen.buffer_empty:
        print(tft_featherwing.touchscreen.read_data())
