# SPDX-FileCopyrightText: Copyright (c) 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Grid layout demo for MacroPad. Displays the key pressed in a grid matching the key layout on the
built-in display.
"""
import displayio
import terminalio
from adafruit_display_text import bitmap_label as label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_macropad import MacroPad

macropad = MacroPad()

main_group = displayio.Group()
macropad.display.root_group = main_group
title = label.Label(
    y=4,
    font=terminalio.FONT,
    color=0x0,
    text="      KEYPRESSES      ",
    background_color=0xFFFFFF,
)
layout = GridLayout(x=0, y=10, width=128, height=54, grid_size=(3, 4), cell_padding=1)
labels = []
for _ in range(12):
    labels.append(label.Label(terminalio.FONT, text=""))

for index in range(12):
    x = index % 3
    y = index // 3
    layout.add_content(labels[index], grid_position=(x, y), cell_size=(1, 1))

main_group.append(title)
main_group.append(layout)

while True:
    key_event = macropad.keys.events.get()
    if key_event:
        if key_event.pressed:
            labels[key_event.key_number].text = "KEY{}".format(key_event.key_number)
        else:
            labels[key_event.key_number].text = ""
