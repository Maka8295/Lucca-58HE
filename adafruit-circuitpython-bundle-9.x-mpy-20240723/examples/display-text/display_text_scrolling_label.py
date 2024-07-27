# SPDX-FileCopyrightText: 2022 Tim Cocks for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import terminalio
from adafruit_display_text.scrolling_label import ScrollingLabel


text = "Hello world CircuitPython scrolling label"
my_scrolling_label = ScrollingLabel(
    terminalio.FONT, text=text, max_characters=20, animate_time=0.3
)
my_scrolling_label.x = 10
my_scrolling_label.y = 10
board.DISPLAY.root_group = my_scrolling_label
while True:
    my_scrolling_label.update()
