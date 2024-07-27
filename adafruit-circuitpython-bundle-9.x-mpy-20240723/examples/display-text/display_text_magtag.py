# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Basic display_text.label example script
adapted for use on MagTag.
"""
import time
import board
import displayio
import terminalio
from adafruit_display_text import label

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

# wait until we can draw
time.sleep(display.time_to_refresh)

# main group to hold everything
main_group = displayio.Group()

# white background. Scaled to save RAM
bg_bitmap = displayio.Bitmap(display.width // 8, display.height // 8, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(bg_bitmap, x=0, y=0, pixel_shader=bg_palette)
bg_group = displayio.Group(scale=8)
bg_group.append(bg_sprite)
main_group.append(bg_group)

# first example label
TEXT = "Hello world"
text_area = label.Label(
    terminalio.FONT,
    text=TEXT,
    color=0xFFFFFF,
    background_color=0x666666,
    padding_top=1,
    padding_bottom=3,
    padding_right=4,
    padding_left=4,
)
text_area.x = 10
text_area.y = 14
main_group.append(text_area)

# second example label
another_text = label.Label(
    terminalio.FONT,
    scale=2,
    text="MagTag display_text\nexample",
    color=0x000000,
    background_color=0x999999,
    padding_top=1,
    padding_bottom=3,
    padding_right=4,
    padding_left=4,
)
# centered
another_text.anchor_point = (0.5, 0.5)
another_text.anchored_position = (display.width // 2, display.height // 2)
main_group.append(another_text)

# show the main group and refresh.
display.root_group = main_group
display.refresh()
while True:
    pass
