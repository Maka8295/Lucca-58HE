# SPDX-FileCopyrightText: 2022 CedarGroveMakerStudios for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Simple painting demo that draws on an Adafruit 2.4" TFT FeatherWing
display (#3315) with the STMPE610 resistive touch controller.
"""

import board
import digitalio
import displayio
from adafruit_rgb_display import ili9341, color565
import adafruit_stmpe610

# Release any resources currently in use for the display
displayio.release_displays()

# Instantiate the 2.4" 320x240 TFT FeatherWing Display(#3315).
cs_pin = digitalio.DigitalInOut(board.D9)
dc_pin = digitalio.DigitalInOut(board.D10)
display = ili9341.ILI9341(board.SPI(), cs=cs_pin, dc=dc_pin)

# Fill the screen with black!
display.fill(color565(0, 0, 0))

# Instantiate the touchpad
ts_cs_pin = digitalio.DigitalInOut(board.D6)
ts = adafruit_stmpe610.Adafruit_STMPE610_SPI(
    board.SPI(),
    ts_cs_pin,
    calibration=((350, 3500), (350, 3500)),
    size=(display.width, display.height),
    disp_rotation=90,
    touch_flip=(True, True),
)

while True:
    point = ts.touch_point
    if point:
        # Display the touched point
        x = point[0]
        y = point[1]
        display.fill_rectangle(x - 2, y - 2, 4, 4, color565(255, 0, 0))
