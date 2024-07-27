# SPDX-FileCopyrightText: 2022 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Simple button demonstration/example.
STMPE610 touch controller with TFT FeatherWing Display

Author(s): ladyada, CedarGroveMakerStudios

"""

import time
import board
import digitalio
import displayio
import terminalio

# from adafruit_hx8357 import HX8357
from adafruit_ili9341 import ILI9341
from adafruit_button import Button
import adafruit_stmpe610

# --| Button Config |-------------------------------------------------
BUTTON_X = 50
BUTTON_Y = 50
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_STYLE = Button.ROUNDRECT
BUTTON_FILL_COLOR = 0x00FFFF
BUTTON_OUTLINE_COLOR = 0xFF00FF
BUTTON_LABEL = "HELLO WORLD"
BUTTON_LABEL_COLOR = 0x000000
# --| Button Config |-------------------------------------------------

# Release any resources currently in use for the displays
displayio.release_displays()
disp_bus = displayio.FourWire(
    board.SPI(), command=board.D10, chip_select=board.D9, reset=None
)

# Instantiate the 2.4" 320x240 TFT FeatherWing (#3315).
display = ILI9341(disp_bus, width=320, height=240)
_touch_flip = (False, False)

"""# Instantiate the 3.5" 480x320 TFT FeatherWing (#3651).
display = HX8357(disp_bus, width=480, height=320)
_touch_flip = (False, True)"""

# Always set rotation before instantiating the touchscreen
display.rotation = 0

# Instantiate touchscreen
ts_cs = digitalio.DigitalInOut(board.D6)
ts = adafruit_stmpe610.Adafruit_STMPE610_SPI(
    board.SPI(),
    ts_cs,
    calibration=((357, 3812), (390, 3555)),
    size=(display.width, display.height),
    disp_rotation=display.rotation,
    touch_flip=_touch_flip,
)

# Create the displayio group and show it
splash = displayio.Group()
display.root_group = splash

# Defiine the button
button = Button(
    x=BUTTON_X,
    y=BUTTON_Y,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    style=BUTTON_STYLE,
    fill_color=BUTTON_FILL_COLOR,
    outline_color=BUTTON_OUTLINE_COLOR,
    label=BUTTON_LABEL,
    label_font=terminalio.FONT,
    label_color=BUTTON_LABEL_COLOR,
)

# Add button to the displayio group
splash.append(button)

# Loop and look for touches
while True:
    p = ts.touch_point
    if p:
        if button.contains(p):
            button.selected = True
            # Perform a task related to the button press here
            time.sleep(0.25)  # Wait a bit so we can see the button color change
        else:
            button.selected = False  # When touch moves outside of button
    else:
        button.selected = False  # When button is released
