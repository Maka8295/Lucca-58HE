# SPDX-FileCopyrightText: 2023 Tim C
# SPDX-License-Identifier: MIT

import board
import terminalio
from adafruit_display_text import outlined_label

if board.DISPLAY.width <= 150:
    text = "Hello\nworld"
else:
    text = "Hello world"

text_area = outlined_label.OutlinedLabel(
    terminalio.FONT,
    text=text,
    color=0xFF00FF,
    outline_color=0x00FF00,
    outline_size=1,
    padding_left=2,
    padding_right=2,
    padding_top=2,
    padding_bottom=2,
    scale=3,
)
text_area.anchor_point = (0, 0)
text_area.anchored_position = (10, 10)
board.DISPLAY.root_group = text_area
while True:
    pass
