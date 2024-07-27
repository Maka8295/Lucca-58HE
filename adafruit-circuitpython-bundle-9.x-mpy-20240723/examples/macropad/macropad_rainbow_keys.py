# SPDX-FileCopyrightText: Copyright (c) 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Rainbow LED grid layout demo for MacroPad. Displays the key pressed in a grid matching the key
layout on the built-in display, and animates a rainbow the first time you press a key and turns it
off on the next press.
"""
import displayio
import terminalio
from rainbowio import colorwheel
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
layout = GridLayout(x=0, y=10, width=128, height=54, grid_size=(3, 4), cell_padding=5)
labels = []
for _ in range(12):
    labels.append(label.Label(terminalio.FONT, text=""))

for index in range(12):
    x = index % 3
    y = index // 3
    layout.add_content(labels[index], grid_position=(x, y), cell_size=(1, 1))

main_group.append(title)
main_group.append(layout)

lit_keys = [False] * 12
wheel_offset = 0
while True:
    key_event = macropad.keys.events.get()
    if key_event:
        if key_event.pressed:
            labels[key_event.key_number].text = "KEY{}".format(key_event.key_number)
            # Turn the LED on with the first press, and off with the second press.
            lit_keys[key_event.key_number] = not lit_keys[key_event.key_number]
        else:
            labels[key_event.key_number].text = ""

    wheel_offset += 1  # Glow thru the colorwheel.
    for pixel in range(12):
        if lit_keys[pixel]:  # Animate the specific LED.
            macropad.pixels[pixel] = colorwheel((pixel / 12 * 256) + wheel_offset)
        else:
            macropad.pixels[pixel] = 0  # Otherwise, turn the LED off.
