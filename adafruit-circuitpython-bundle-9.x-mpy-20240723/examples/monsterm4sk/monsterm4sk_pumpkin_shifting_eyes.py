# SPDX-FileCopyrightText: 2020 Foamyguy, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
CircuitPython example for Monster M4sk.

Draws a yellow triangle on each screen as Jack-O-Lantern eyes.
The eyes shift back and forth from left to right.
"""

import time
import board
import displayio
import adafruit_imageload
import adafruit_monsterm4sk

SCREEN_SIZE = 240
IMAGE_SIZE = 173

# Create a bitmap for the background 10x10 pixels
bg_color_pixel = displayio.Bitmap(10, 10, 1)

# Create a two color palette
bg_palette = displayio.Palette(2)
bg_palette[0] = 0xFF7700  # orange

bg_color_pixel.fill(0)  # fill orange

# Create a TileGrid for the orange background
bg_left_tile_grid = displayio.TileGrid(bg_color_pixel, pixel_shader=bg_palette)
bg_right_tile_grid = displayio.TileGrid(bg_color_pixel, pixel_shader=bg_palette)

# Create background groups scaled 24x to match screen size
bg_left_group = displayio.Group(scale=24)
bg_right_group = displayio.Group(scale=24)

# add the background tilegrids to the scaled groups
bg_left_group.append(bg_left_tile_grid)
bg_right_group.append(bg_right_tile_grid)

# load the eye image
eye_image, eye_palette = adafruit_imageload.load(
    "/small_triangle_eye.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
)

# Create a TileGrid to hold the bitmap for each eye
right_pumkin_eye_tilegrid = displayio.TileGrid(eye_image, pixel_shader=eye_palette)
left_pumkin_eye_tilegrid = displayio.TileGrid(eye_image, pixel_shader=eye_palette)

# initialize the monster m4sk hardware
i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
mask = adafruit_monsterm4sk.MonsterM4sk(i2c=i2c_bus)

# left eye group setup
left_group = displayio.Group()
mask.left_display.root_group = left_group

# right eye group setup
right_group = displayio.Group()
mask.right_display.root_group = right_group

# Add orange backgrounds to both groups
right_group.append(bg_right_group)
left_group.append(bg_left_group)

# add triangle eyes to both groups
right_group.append(right_pumkin_eye_tilegrid)
left_group.append(left_pumkin_eye_tilegrid)

# centered vertically
right_pumkin_eye_tilegrid.y = (SCREEN_SIZE - IMAGE_SIZE) // 2
left_pumkin_eye_tilegrid.y = (SCREEN_SIZE - IMAGE_SIZE) // 2

while True:
    # move the eyes to the right
    for i in range(0, 240 - 173, 5):
        right_pumkin_eye_tilegrid.x = i
        left_pumkin_eye_tilegrid.x = i
        time.sleep(0.01)

    time.sleep(2)  # wait 2 seconds

    # move the eyes to the left
    for i in range(0, 240 - 173, 5):
        right_pumkin_eye_tilegrid.x -= 5
        left_pumkin_eye_tilegrid.x -= 5
        time.sleep(0.01)

    time.sleep(2)  # wait 2 seconds

    if mask.boop:
        pass

    if mask.buttons["S9"]:
        pass

    if mask.buttons["S10"]:
        pass

    if mask.buttons["S11"]:
        pass
