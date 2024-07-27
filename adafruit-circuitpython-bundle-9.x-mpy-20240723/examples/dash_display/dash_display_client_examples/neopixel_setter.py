# SPDX-FileCopyrightText: 2021 Eva Herrada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from adafruit_funhouse import FunHouse
from adafruit_display_shapes.rect import Rect

funhouse = FunHouse(default_bg=None)

funhouse.display.root_group = None
rect = Rect(31, 105, 30, 30, fill=0xFFFFFF)
funhouse.splash.append(rect)
R_label = funhouse.add_text(
    text="   +\nR:\n   -", text_position=(5, 120), text_scale=2, text_color=0xFFFFFF
)
G_label = funhouse.add_text(
    text="   +\nG:\n   -", text_position=(90, 120), text_scale=2, text_color=0xFFFFFF
)
B_label = funhouse.add_text(
    text="   +\nB:\n   -", text_position=(175, 120), text_scale=2, text_color=0xFFFFFF
)
R = funhouse.add_text(
    text="00", text_position=(35, 120), text_scale=2, text_color=0x000000
)
G = funhouse.add_text(
    text="00", text_position=(120, 120), text_scale=2, text_color=0x000000
)
B = funhouse.add_text(
    text="00", text_position=(205, 120), text_scale=2, text_color=0x000000
)
funhouse.display.root_group = funhouse.splash

index = 0
colors = [00, 00, 00]
while True:
    if funhouse.peripherals.button_sel:
        index += 1
        if index == 3:
            index = 0
        time.sleep(0.1)

    if funhouse.peripherals.button_up:
        colors[index] += 1
        if colors[index] == 256:
            colors[index] = 0
        funhouse.set_text(hex(colors[index])[2:], index + 3)

    if funhouse.peripherals.button_down:
        colors[index] -= 1
        if colors[index] == -1:
            colors[index] = 255
        funhouse.set_text(hex(colors[index])[2:], index + 3)

    if funhouse.peripherals.captouch8:
        color = ["{:02x}".format(colors[i]) for i in range(len(colors))]
        color = "#" + "".join(color)
        break

    if funhouse.peripherals.captouch7:
        break

    rect.x = 85 * index + 31
    time.sleep(0.01)
