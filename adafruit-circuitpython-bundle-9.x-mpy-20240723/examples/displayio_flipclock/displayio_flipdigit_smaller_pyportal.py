# SPDX-FileCopyrightText: Copyright (c) 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Most basic example showing how to initialize and use the FlipDigit displayio object.
"""
import gc
import time
from displayio import Group
import board
import adafruit_imageload
from adafruit_displayio_flipclock.flip_digit import FlipDigit


#  == Configuration Variables ==

# seconds per animation frame
ANIMATION_DELAY = 0.02

# number of frames in the animation
ANIMATION_FRAME_COUNT = 5

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

# group to hold our flip digit
main_group = Group()

# load the static sprite sheet
static_spritesheet, static_palette = adafruit_imageload.load("static_sheet_small.bmp")
static_palette.make_transparent(0)

gc.collect()
# print(gc.mem_free())
# load the animation sprite sheets
top_animation_spritesheet, top_animation_palette = adafruit_imageload.load(
    "top_animation_sheet_small_5frames.bmp"
)
gc.collect()
# print(gc.mem_free())
bottom_animation_spritesheet, bottom_animation_palette = adafruit_imageload.load(
    "bottom_animation_sheet_small_5frames.bmp"
)

# set the transparent color indexes in respective palettes
for i in TRANSPARENT_INDEXES:
    top_animation_palette.make_transparent(i)
    bottom_animation_palette.make_transparent(i)

# calculate sprite size by dividing total sheet
SPRITE_WIDTH = static_spritesheet.width // 3
SPRITE_HEIGHT = (static_spritesheet.height // 4) // 2

print(f"w: {SPRITE_WIDTH}, h: {SPRITE_HEIGHT}")

# initialize FlipDigit widget object
flip_digit = FlipDigit(
    static_spritesheet,
    static_palette,
    top_animation_spritesheet,
    top_animation_palette,
    bottom_animation_spritesheet,
    bottom_animation_palette,
    SPRITE_WIDTH,
    SPRITE_HEIGHT,
    anim_frame_count=ANIMATION_FRAME_COUNT,
    anim_delay=ANIMATION_DELAY,
    dynamic_fading=True,
    brighter_level=BRIGHTER_LEVEL,
    darker_level=DARKER_LEVEL,
    medium_level=MEDIUM_LEVEL,
)

flip_digit.scale = 4

# position it in the center of the display
flip_digit.anchor_point = (0.5, 0.5)
flip_digit.anchored_position = (display.width // 2, display.height // 2)

# add it to the group
main_group.append(flip_digit)

# show the group on the display
display.root_group = main_group


while True:
    # loop over values 0-9
    for i in range(10):
        # update the value in the flip digit
        flip_digit.value = i
        time.sleep(0.75)
