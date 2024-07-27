# SPDX-FileCopyrightText: 2021 Tim Cocks for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Basic example that illustrates how to set the various color options on the button using
properties after the button has been initialized.
"""

import board
import displayio
import terminalio
import adafruit_touchscreen
from adafruit_button import Button

# use built in display (MagTag, PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

# --| Button Config |-------------------------------------------------
BUTTON_X = 110
BUTTON_Y = 95
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_STYLE = Button.ROUNDRECT
BUTTON_FILL_COLOR = 0xAA0000
BUTTON_OUTLINE_COLOR = 0x0000FF
BUTTON_LABEL = "HELLO WORLD"
BUTTON_LABEL_COLOR = 0x000000
# --| Button Config |-------------------------------------------------

# Setup touchscreen (PyPortal)
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(display.width, display.height),
)

# Make the display context
splash = displayio.Group()
display.root_group = splash

# Make the button
button = Button(
    x=BUTTON_X,
    y=BUTTON_Y,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    style=BUTTON_STYLE,
    fill_color=BUTTON_FILL_COLOR,
    outline_color=BUTTON_OUTLINE_COLOR,
    label="HELLO WORLD",
    label_font=terminalio.FONT,
    label_color=BUTTON_LABEL_COLOR,
)

button.fill_color = 0x00FF00
button.outline_color = 0xFF0000

button.selected_fill = (0, 0, 255)
button.selected_outline = (255, 0, 0)

button.label_color = 0xFF0000
button.selected_label = 0x00FF00

# Add button to the display context
splash.append(button)

# Loop and look for touches
while True:
    p = ts.touch_point
    if p:
        if button.contains(p):
            print(p)
            button.selected = True
    else:
        button.selected = False
