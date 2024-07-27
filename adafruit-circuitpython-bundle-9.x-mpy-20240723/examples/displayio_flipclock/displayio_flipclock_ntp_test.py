# SPDX-FileCopyrightText: Copyright (c) 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Advanced example that shows how you can use the
FlipClock displayio object along with the adafruit_ntp library
to show and update the current time with a FlipClock on a display.
"""

import time
import board
import socketpool
import wifi
from displayio import Group
import adafruit_imageload
import adafruit_ntp
from adafruit_displayio_flipclock.flip_clock import FlipClock

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

ANIMATION_DELAY = 0.01
TRANSPARENT_INDEXES = range(11)
BRIGHTER_LEVEL = 0.99
DARKER_LEVEL = 0.5
MEDIUM_LEVEL = 0.9
UTC_OFFSET = -5

wifi.radio.connect(secrets["ssid"], secrets["password"])
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=UTC_OFFSET)


display = board.DISPLAY

static_spritesheet, static_palette = adafruit_imageload.load("static_sheet.bmp")
static_palette.make_transparent(0)

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

SPRITE_WIDTH = static_spritesheet.width // 3
SPRITE_HEIGHT = (static_spritesheet.height // 4) // 2

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
    #    transparent_indexes=TRANSPARENT_INDEXES,
    brighter_level=BRIGHTER_LEVEL,
    darker_level=DARKER_LEVEL,
    medium_level=MEDIUM_LEVEL,
)

clock.anchor_point = (0.5, 0.5)
clock.anchored_position = (display.width // 2, display.height // 2)

main_group = Group()
main_group.append(clock)
board.DISPLAY.root_group = main_group

while True:
    try:
        cur_time = ntp.datetime
        clock.first_pair = str(cur_time.tm_hour)
        clock.second_pair = str(cur_time.tm_min)
    except (OSError, ValueError):
        # no problem, try again next time.
        pass
    time.sleep(10)
