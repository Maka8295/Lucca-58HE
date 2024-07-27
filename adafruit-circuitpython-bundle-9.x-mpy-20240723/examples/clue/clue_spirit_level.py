# SPDX-FileCopyrightText: 2019 Kattni Rembor, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""CLUE Spirit Level Demo"""
import board
import displayio
from adafruit_display_shapes.circle import Circle
from adafruit_clue import clue

display = board.DISPLAY
clue_group = displayio.Group()

outer_circle = Circle(120, 120, 119, outline=clue.WHITE)
middle_circle = Circle(120, 120, 75, outline=clue.YELLOW)
inner_circle = Circle(120, 120, 35, outline=clue.GREEN)
clue_group.append(outer_circle)
clue_group.append(middle_circle)
clue_group.append(inner_circle)

x, y, _ = clue.acceleration
bubble_group = displayio.Group()
level_bubble = Circle(int(x + 120), int(y + 120), 20, fill=clue.RED, outline=clue.RED)
bubble_group.append(level_bubble)

clue_group.append(bubble_group)
display.root_group = clue_group

while True:
    x, y, _ = clue.acceleration
    bubble_group.x = int(x * -10)
    bubble_group.y = int(y * -10)
