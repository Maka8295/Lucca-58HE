# SPDX-FileCopyrightText: 2022 flom84 for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import displayio
import terminalio

from adafruit_button import Button
from adafruit_cursorcontrol.cursorcontrol import Cursor
from adafruit_cursorcontrol.cursorcontrol_cursormanager import DebouncedCursorManager

SELECT_BUTTON_X = 0
SELECT_BUTTON_Y = 103
SELECT_BUTTON_WIDTH = 60
SELECT_BUTTON_HEIGHT = 25
SELECT_BUTTON_STYLE = Button.ROUNDRECT
SELECT_BUTTON_OUTLINE_COLOR = 0xFFFFFF
SELECT_BUTTON_LABEL = "Select"
SELECT_BUTTON_LABEL_COLOR = 0xFFFFFF

START_BUTTON_X = 100
START_BUTTON_Y = 103
START_BUTTON_WIDTH = 60
START_BUTTON_HEIGHT = 25
START_BUTTON_STYLE = Button.ROUNDRECT
START_BUTTON_OUTLINE_COLOR = 0xFFFFFF
START_BUTTON_LABEL = "Start"
START_BUTTON_LABEL_COLOR = 0xFFFFFF

A_BUTTON_X = 120
A_BUTTON_Y = 20
A_BUTTON_WIDTH = 30
A_BUTTON_HEIGHT = 30
A_BUTTON_STYLE = Button.ROUNDRECT
A_BUTTON_OUTLINE_COLOR = 0xFFFFFF
A_BUTTON_LABEL = "A"
A_BUTTON_LABEL_COLOR = 0xFFFFFF

B_BUTTON_X = 80
B_BUTTON_Y = 30
B_BUTTON_WIDTH = 30
B_BUTTON_HEIGHT = 30
B_BUTTON_STYLE = Button.ROUNDRECT
B_BUTTON_OUTLINE_COLOR = 0xFFFFFF
B_BUTTON_LABEL = "B"
B_BUTTON_LABEL_COLOR = 0xFFFFFF

BUTTON_FILL_PURPLE = 0xB400FF
BUTTON_FILL_BLACK = 0x000000

start_button = Button(
    x=START_BUTTON_X,
    y=START_BUTTON_Y,
    width=START_BUTTON_WIDTH,
    height=START_BUTTON_HEIGHT,
    style=START_BUTTON_STYLE,
    fill_color=BUTTON_FILL_BLACK,
    outline_color=START_BUTTON_OUTLINE_COLOR,
    label=START_BUTTON_LABEL,
    label_font=terminalio.FONT,
    label_color=START_BUTTON_LABEL_COLOR,
)

select_button = Button(
    x=SELECT_BUTTON_X,
    y=SELECT_BUTTON_Y,
    width=SELECT_BUTTON_WIDTH,
    height=SELECT_BUTTON_HEIGHT,
    style=SELECT_BUTTON_STYLE,
    fill_color=BUTTON_FILL_BLACK,
    outline_color=SELECT_BUTTON_OUTLINE_COLOR,
    label=SELECT_BUTTON_LABEL,
    label_font=terminalio.FONT,
    label_color=SELECT_BUTTON_LABEL_COLOR,
)

a_button = Button(
    x=A_BUTTON_X,
    y=A_BUTTON_Y,
    width=A_BUTTON_WIDTH,
    height=A_BUTTON_HEIGHT,
    style=A_BUTTON_STYLE,
    fill_color=BUTTON_FILL_BLACK,
    outline_color=A_BUTTON_OUTLINE_COLOR,
    label=A_BUTTON_LABEL,
    label_font=terminalio.FONT,
    label_color=A_BUTTON_LABEL_COLOR,
)

b_button = Button(
    x=B_BUTTON_X,
    y=B_BUTTON_Y,
    width=B_BUTTON_WIDTH,
    height=B_BUTTON_HEIGHT,
    style=B_BUTTON_STYLE,
    fill_color=BUTTON_FILL_BLACK,
    outline_color=B_BUTTON_OUTLINE_COLOR,
    label=B_BUTTON_LABEL,
    label_font=terminalio.FONT,
    label_color=B_BUTTON_LABEL_COLOR,
)

# Create the display
display = board.DISPLAY

# Create the display context
splash = displayio.Group()

# initialize the mouse cursor object
mouse_cursor = Cursor(display, display_group=splash)

# initialize the debounced cursor manager
debounced_cursor = DebouncedCursorManager(mouse_cursor)

# create displayio group
splash.append(start_button)
splash.append(select_button)
splash.append(a_button)
splash.append(b_button)
display.root_group = splash

while True:
    debounced_cursor.update()

    if debounced_cursor.is_clicked:
        a_button.fill_color = BUTTON_FILL_PURPLE
        print("A pressed:  " + str(debounced_cursor.held))

    if debounced_cursor.released:
        a_button.fill_color = BUTTON_FILL_BLACK
        print("A pressed:  " + str(debounced_cursor.held))

    if debounced_cursor.is_alt_clicked:
        b_button.fill_color = BUTTON_FILL_PURPLE
        print("B pressed:  " + str(debounced_cursor.alt_held))

    if debounced_cursor.alt_released:
        b_button.fill_color = BUTTON_FILL_BLACK
        print("B pressed:  " + str(debounced_cursor.alt_held))

    if debounced_cursor.is_start_clicked:
        start_button.fill_color = BUTTON_FILL_PURPLE
        print("Start pressed: " + str(debounced_cursor.start_held))

    if debounced_cursor.start_released:
        start_button.fill_color = BUTTON_FILL_BLACK
        print("Start pressed: " + str(debounced_cursor.start_held))

    if debounced_cursor.is_select_clicked:
        select_button.fill_color = BUTTON_FILL_PURPLE
        print("Select pressed:  " + str(debounced_cursor.select_held))

    if debounced_cursor.select_released:
        select_button.fill_color = BUTTON_FILL_BLACK
        print("Select pressed:  " + str(debounced_cursor.select_held))

    time.sleep(0.01)
