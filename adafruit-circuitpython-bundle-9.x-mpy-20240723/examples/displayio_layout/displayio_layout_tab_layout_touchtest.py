# SPDX-FileCopyrightText: 2022 Tim C
#
# SPDX-License-Identifier: MIT
"""
Make a TabLayout change tabs with the touchscreen
"""
import displayio
import board
import terminalio
import adafruit_touchscreen
from adafruit_display_text.bitmap_label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle
from adafruit_displayio_layout.layouts.tab_layout import TabLayout

# built-in display
display = board.DISPLAY

# ------------ Touchscreen setup --------------- #
# See: https://learn.adafruit.com/making-a-pyportal-user-interface-displayio/display
display = board.DISPLAY  # create the display object

screen_width = display.width
screen_height = display.height
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(screen_width, screen_height),
)

# create and show main_group
main_group = displayio.Group()
display.root_group = main_group

font = terminalio.FONT

# create the page layout
test_page_layout = TabLayout(
    x=0,
    y=0,
    display=board.DISPLAY,
    tab_text_scale=2,
    custom_font=font,
    inactive_tab_spritesheet="bmps/inactive_tab_sprite.bmp",
    showing_tab_spritesheet="bmps/active_tab_sprite.bmp",
    showing_tab_text_color=0x00AA59,
    inactive_tab_text_color=0xEEEEEE,
    inactive_tab_transparent_indexes=(0, 1),
    showing_tab_transparent_indexes=(0, 1),
    tab_count=4,
)

# make page content Groups
page_1_group = displayio.Group()
page_2_group = displayio.Group()
page_3_group = displayio.Group()
page_4_group = displayio.Group()

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
    text="This page is the\nsecond page!",
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

page_4_lbl = Label(
    font=terminalio.FONT,
    scale=2,
    text="The fourth page\nis where it's at",
    anchor_point=(0, 0),
    anchored_position=(10, 10),
)

# shapes
square = Rect(x=20, y=70, width=40, height=40, fill=0x00DD00)
circle = Circle(50, 120, r=30, fill=0xDD00DD)
triangle = Triangle(50, 0, 100, 50, 0, 50, fill=0xDDDD00)
rectangle = Rect(x=80, y=80, width=100, height=50, fill=0x0000DD)

triangle.x = 80
triangle.y = 70

# add everything to their page groups
page_1_group.append(square)
page_1_group.append(page_1_lbl)
page_2_group.append(page_2_lbl)
page_2_group.append(circle)
page_3_group.append(page_3_lbl)
page_3_group.append(triangle)
page_4_group.append(page_4_lbl)
page_4_group.append(rectangle)

# add the pages to the layout, supply your own page names
test_page_layout.add_content(page_1_group, "One")
test_page_layout.add_content(page_2_group, "Two")
test_page_layout.add_content(page_3_group, "Thr")
test_page_layout.add_content(page_4_group, "For")

# add it to the group that is showing on the display
main_group.append(test_page_layout)


# add something new after the TabLayout was already created
another_text = Label(
    terminalio.FONT,
    text="And another thing!",
    scale=2,
    color=0x00FF00,
    anchor_point=(0, 0),
    anchored_position=(100, 100),
)
test_page_layout.showing_page_content.append(another_text)

while True:
    touch = ts.touch_point
    if touch:
        test_page_layout.handle_touch_events(touch)
