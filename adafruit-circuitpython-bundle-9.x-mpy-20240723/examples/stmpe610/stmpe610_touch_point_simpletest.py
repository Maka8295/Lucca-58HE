# SPDX-FileCopyrightText: 2022 CedarGroveMakerStudios for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Simple print-to-REPL demo using the STMPE610 resistive touch controller.
"""

import board
import digitalio
import adafruit_stmpe610

# Instantiate the touchpad
ts_cs_pin = digitalio.DigitalInOut(board.D6)
ts = adafruit_stmpe610.Adafruit_STMPE610_SPI(board.SPI(), ts_cs_pin)

print("Go Ahead - Touch the Screen - Make My Day!")
print("(x, y, pressure)")
while True:
    point = ts.touch_point
    if point:
        print(point)
