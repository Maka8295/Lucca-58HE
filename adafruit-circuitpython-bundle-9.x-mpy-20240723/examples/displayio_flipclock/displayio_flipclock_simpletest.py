# SPDX-FileCopyrightText: Copyright (c) 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
An example that shows how to initialize and use the FlipClock displayio object.

This example is the most basic usage of FlipClock and is not intended to count
time or any other specific units or values.
"""
import time
import board
from displayio import Group
import adafruit_imageload
from adafruit_displayio_flipclock.flip_clock import FlipClock

#  == Configuration Variables ==

# seconds per animation frame
ANIMATION_DELAY = 0.01

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

# set a value to start with in the first pair
clock.first_pair = "13"

while True:
    # increment first pair number
    cur_val = clock.first_pair
    next_val = int(cur_val) + 1

    # if it's time to reset
    if next_val > 20:
        # reset value back to 0
        next_val = 0

    # set the first pair value on the FlipClock
    clock.first_pair = str(next_val)

    # increment second pair value
    cur_val = clock.second_pair
    next_val = int(cur_val) + 1

    # if it's time to reset
    if next_val > 99:
        # reset value back to 0
        next_val = 0

    # set the second pair value on the FlipClock
    clock.second_pair = str(next_val)

    time.sleep(0.5)
