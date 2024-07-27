# SPDX-FileCopyrightText: 2023 Bernhard Bablok
# SPDX-License-Identifier: MIT

import time
import board

import displayio
from adafruit_display_shapes.arc import Arc
from adafruit_display_shapes.circle import Circle

# use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

w2 = int(display.width / 2)
h2 = int(display.height / 2)

WHITE = 0xFFFFFF
RED = 0xFF0000
GREEN = 0x00FF00
BLUE = 0x0000FF

# Make the display context
group = displayio.Group()
display.root_group = group

# little circle in the center of all arcs
circle = Circle(w2, h2, 5, fill=0xFF0000, outline=0xFF0000)
group.append(circle)

# red arc with white outline, 10 pixels wide
arc1 = Arc(
    x=w2,
    y=h2,
    radius=min(display.width, display.height) / 4,
    angle=90,
    direction=90,
    segments=10,
    arc_width=10,
    outline=WHITE,
    fill=RED,
)
group.append(arc1)

# green arc (single line)
arc2 = Arc(
    x=w2,
    y=h2,
    radius=min(display.width, display.height) / 4 + 5,
    angle=180,
    direction=90,
    segments=20,
    arc_width=1,
    outline=GREEN,
)
group.append(arc2)

# blue arc (or pie)
arc3 = Arc(
    x=w2,
    y=h2,
    radius=min(display.width, display.height) / 4,
    angle=90,
    direction=-90,
    segments=10,
    arc_width=min(display.width, display.height) / 4 - 5,
    outline=BLUE,
)
group.append(arc3)

while True:
    time.sleep(0.1)
