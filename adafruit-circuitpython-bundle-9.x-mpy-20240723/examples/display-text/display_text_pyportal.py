# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example show the use of the backlight as well as using labels to simulate
a terminal using a font on the PyPortal
"""

import os
import time
import board
import displayio

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label

FONT_DIR = "/fonts/"
fonts = list(
    filter(lambda x: x.endswith("bdf") and not x.startswith("."), os.listdir(FONT_DIR))
)
fonts = [bitmap_font.load_font(FONT_DIR + x) for x in fonts]
if len(fonts) == 0:
    print("No fonts found in '{}'".format(FONT_DIR))

print("fade up")
# Fade up the backlight
for b in range(100):
    board.DISPLAY.brightness = b / 100
    time.sleep(0.01)  # default (0.01)

demos = ["CircuitPython = Code + Community", "accents - üàêùéáçãÍóí", "others - αψ◌"]

splash = displayio.Group()
board.DISPLAY.root_group = splash
max_y = 0
y = 0
for demo_text in demos:
    for font in fonts:
        if y >= board.DISPLAY.height:
            y = 0
            while len(splash):
                splash.pop()
        print("Font load {}".format(font.name))
        area = Label(
            font, text=demo_text, anchor_point=(0, 0), anchored_position=(0, y)
        )
        splash.append(area)

        y += area.height

        # Wait for the image to load.
        try:
            board.DISPLAY.refresh(target_frames_per_second=60)
        except AttributeError:
            board.DISPLAY.wait_for_frame()

# Wait for 1 minute (60 seconds)
time.sleep(60)

# Fade down the backlight
for b in range(100, -1, -1):
    board.DISPLAY.brightness = b / 100
    time.sleep(0.01)  # default (0.01)

print("fade down")

time.sleep(10)
