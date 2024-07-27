# SPDX-FileCopyrightText: 2022 Tim C
#
# SPDX-License-Identifier: MIT
"""
Make a PageLayout with two pages and change between them.
"""
import time
import displayio
import board
import terminalio
from adafruit_display_text.bitmap_label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_displayio_layout.layouts.page_layout import PageLayout

# built-in display
display = board.DISPLAY

# create and show main_group
main_group = displayio.Group()
display.root_group = main_group

# create the page layout
test_page_layout = PageLayout(x=0, y=0)

page_1_lbl = Label(
    font=terminalio.FONT,
    scale=2,
    text="This is the first page!",
    anchor_point=(0, 0),
    anchored_position=(10, 10),
)
page_2_lbl = Label(
    font=terminalio.FONT,
    scale=2,
    text="This page is the second page!",
    anchor_point=(0, 0),
    anchored_position=(10, 10),
)

page_1_group = displayio.Group()
page_2_group = displayio.Group()

square = Rect(x=20, y=70, width=40, height=40, fill=0x00DD00)
circle = Circle(50, 100, r=30, fill=0xDD00DD)

page_1_group.append(square)
page_1_group.append(page_1_lbl)

page_2_group.append(page_2_lbl)
page_2_group.append(circle)

test_page_layout.add_content(page_1_group, "page_1")
test_page_layout.add_content(page_2_group, "page_2")

main_group.append(test_page_layout)
while True:
    time.sleep(1)
    test_page_layout.next_page()
