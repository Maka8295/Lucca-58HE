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
bmp = displayio.Bitmap(20, 20, 3)
for i in range(0, bmp.height):
    bmp[0, i] = 1
    bmp[bmp.width - 1, i] = 1
for i in range(0, bmp.width):
    bmp[i, 0] = 1
    bmp[i, bmp.height - 1] = 1

mouse_cursor = Cursor(display, display_group=splash, bmp=bmp)

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
