# SPDX-FileCopyrightText: 2022 Tim C
#
# SPDX-License-Identifier: MIT
"""
Make a PageLayout and illustrate all of it's features
"""
import time
import displayio
import board
import terminalio
from adafruit_display_text.bitmap_label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle
from adafruit_displayio_layout.layouts.page_layout import PageLayout

# built-in display
display = board.DISPLAY

# create and show main_group
main_group = displayio.Group()
display.root_group = main_group

# create the page layout
test_page_layout = PageLayout(x=0, y=0)

# make 3 pages of content
page_1_group = displayio.Group()
page_2_group = displayio.Group()
page_3_group = displayio.Group()

# labels
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
page_3_lbl = Label(
    font=terminalio.FONT,
    scale=2,
    text="The third page is fun!",
    anchor_point=(0, 0),
    anchored_position=(10, 10),
)

# shapes
square = Rect(x=20, y=70, width=40, height=40, fill=0x00DD00)
circle = Circle(50, 100, r=30, fill=0xDD00DD)
triangle = Triangle(50, 0, 100, 50, 0, 50, fill=0xDDDD00)
triangle.x = 80
triangle.y = 70

# add everything to their page groups
page_1_group.append(square)
page_1_group.append(page_1_lbl)
page_2_group.append(page_2_lbl)
page_2_group.append(circle)
page_3_group.append(page_3_lbl)
page_3_group.append(triangle)

# add the pages to the layout, supply your own page names
test_page_layout.add_content(page_1_group, "page_1")
test_page_layout.add_content(page_2_group, "page_2")
test_page_layout.add_content(page_3_group, "page_3")

# add it to the group that is showing on the display
main_group.append(test_page_layout)

# change page with function by name
test_page_layout.show_page(page_name="page_3")
print("showing page index:{}".format(test_page_layout.showing_page_index))
time.sleep(1)

# change page with function by index
test_page_layout.show_page(page_index=0)
print("showing page name: {}".format(test_page_layout.showing_page_name))
time.sleep(1)

# change page by updating the page name property
test_page_layout.showing_page_name = "page_3"
print("showing page index: {}".format(test_page_layout.showing_page_index))
time.sleep(1)

# change page by updating the page index property
test_page_layout.showing_page_index = 1
print("showing page name: {}".format(test_page_layout.showing_page_name))
time.sleep(5)

another_text = Label(
    terminalio.FONT,
    text="And another thing!",
    scale=2,
    color=0x00FF00,
    anchor_point=(0, 0),
    anchored_position=(100, 100),
)
test_page_layout.showing_page_content.append(another_text)

print("starting loop")
while True:
    time.sleep(1)
    # change page by next page function. It will loop by default
    test_page_layout.next_page()
