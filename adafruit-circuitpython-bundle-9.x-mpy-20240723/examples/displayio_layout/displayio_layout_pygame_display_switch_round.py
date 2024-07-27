# SPDX-FileCopyrightText: 2021 Tim C
#
# SPDX-License-Identifier: MIT
"""
Make a GridLayout with some Labels in it's cells.
Displayed with Blinka_Displayio_PyGameDisplay

Requires: https://github.com/FoamyGuy/Blinka_Displayio_PyGameDisplay
"""
import displayio
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_displayio_layout.widgets.switch_round import SwitchRound as Switch


# Make the display context. Change size if you want
display = PyGameDisplay(width=320, height=240)

# Make the display context
main_group = displayio.Group()
display.root_group = main_group

switch_x = 30
switch_y = 30
switch_radius = 20

switch_fill_color_off = (200, 44, 200)
switch_fill_color_on = (0, 100, 0)

switch_outline_color_off = (30, 30, 30)
switch_outline_color_on = (0, 60, 0)

background_color_off = (255, 255, 255)
background_color_on = (90, 255, 90)

background_outline_color_off = background_color_off
background_outline_color_on = background_color_on

switch_width = 4 * switch_radius  # This is a good aspect ratio to start with

switch_stroke = 2  # Width of the outlines (in pixels)
text_stroke = switch_stroke  # width of text lines
touch_padding = 0  # Additional boundary around widget that will accept touch input

animation_time = 0.2  # time for switch to display change (in seconds).
# animation_time=0.15 is a good starting point
display_text = True  # show the text (0/1)

# initialize state variables
switch_value = False
switch_value = True

my_switch = Switch(
    x=switch_x,
    y=switch_y,
    height=switch_radius * 2,
    fill_color_off=switch_fill_color_off,
    fill_color_on=switch_fill_color_on,
    outline_color_off=switch_outline_color_off,
    outline_color_on=switch_outline_color_on,
    background_color_off=background_color_off,
    background_color_on=background_color_on,
    background_outline_color_off=background_outline_color_off,
    background_outline_color_on=background_outline_color_on,
    switch_stroke=switch_stroke,
    display_button_text=display_text,
    touch_padding=10,
    animation_time=animation_time,
    value=False,
)


main_group.append(my_switch)
while display.running:
    # get mouse up  events
    ev = pygame.event.get(eventtype=pygame.MOUSEBUTTONUP)
    # proceed events
    for event in ev:
        pos = pygame.mouse.get_pos()
        print(pos)
        if my_switch.contains(pos):
            my_switch.selected(pos)
