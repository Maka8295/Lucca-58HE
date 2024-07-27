# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import displayio
from adafruit_cursorcontrol.cursorcontrol import Cursor
from adafruit_cursorcontrol.cursorcontrol_cursormanager import CursorManager

# Create the display
display = board.DISPLAY

# Create the display context
splash = displayio.Group()

# initialize the mouse cursor object
mouse_cursor = Cursor(display, display_group=splash)

# initialize the cursormanager
cursor = CursorManager(mouse_cursor)

# show displayio group
display.root_group = splash

while True:
    cursor.update()
    if cursor.is_clicked:
        if mouse_cursor.hidden:
            mouse_cursor.show()
        else:
            mouse_cursor.hide()
    time.sleep(0.01)
