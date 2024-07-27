# SPDX-FileCopyrightText: Copyright (c) 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
An example that shows how you can use the FlipClock displayio
object to represent hours and minutes values.

Note that it's not counting at realtime speed, and it doesn't
know the current hour/minute. This example is only showing the logic
needed to count time with the FlipClock
"""
import time
import board
from displayio import Group
import adafruit_imageload
from adafruit_displayio_flipclock.flip_clock import FlipClock

#  == Configuration Variables ==

# seconds per animation frame
ANIMATION_DELAY = 0.02

# number of frames in the animation
ANIMATION_FRAME_COUNT = 10

# color indexes that will be made transparent in the palette
TRANSPARENT_INDEXES = range(11)

# Brightness modifier for top half during animation
BRIGHTER_LEVEL = 0.99

# Brightness modifier for bottom half in the shadow during animation
DARKER_LEVEL = 0.5

# Brightness modifier to use by default for static sprites
MEDIUM_LEVEL = 0.9

# == END configuration variables ==

# access built-in display
display = board.DISPLAY

# load the static sprite sheet
static_spritesheet, static_palette = adafruit_imageload.load("static_sheet.bmp")
static_palette.make_transparent(0)

# load the animation sprite sheets
top_animation_spritesheet, top_animation_palette = adafruit_imageload.load(
    "grey_top_animation_sheet.bmp"
)
bottom_animation_spritesheet, bottom_animation_palette = adafruit_imageload.load(
    "grey_bottom_animation_sheet.bmp"
)

# set the transparent color indexes in respective palettes
for i in TRANSPARENT_INDEXES:
    top_animation_palette.make_transparent(i)
    bottom_animation_palette.make_transparent(i)

# calculate sprite size by dividing total sheet
SPRITE_WIDTH = static_spritesheet.width // 3
SPRITE_HEIGHT = (static_spritesheet.height // 4) // 2

# initialize FlipClock widget object
clock = FlipClock(
    static_spritesheet,
    static_palette,
    top_animation_spritesheet,
    top_animation_palette,
    bottom_animation_spritesheet,
    bottom_animation_palette,
    SPRITE_WIDTH,
    SPRITE_HEIGHT,
    anim_delay=ANIMATION_DELAY,
    brighter_level=BRIGHTER_LEVEL,
    darker_level=DARKER_LEVEL,
    medium_level=MEDIUM_LEVEL,
)

# position it in the center of the display
clock.anchor_point = (0.5, 0.5)
clock.anchored_position = (display.width // 2, display.height // 2)

# group to hold our flip clock
main_group = Group()

# append the clock to the group
main_group.append(clock)

# show the group on the display
board.DISPLAY.root_group = main_group

# variables to store hours and minutes values
cur_hour = clock.first_pair
cur_minute = clock.second_pair
next_minute = None
next_hour = None

while True:
    # increment minute value
    cur_minute = clock.second_pair
    next_minute = int(cur_minute) + 1

    # if it's time to wrap minutes space
    if next_minute > 59:
        # reset next minute to 0
        next_minute = 0

        # set the minute value on the flip clock
        clock.second_pair = str(next_minute)

        # increment hour value
        cur_hour = clock.first_pair
        next_hour = int(cur_hour) + 1

        # if it's time to wrap hours space
        if next_hour > 23:
            # reset hour to 0
            next_hour = 0

        # set the hour value on the flip clock
        clock.first_pair = str(next_hour)

    else:  # not ready to wrap minutes yet
        # set minute value on the flip clock
        clock.second_pair = str(next_minute)
    time.sleep(0.1)
