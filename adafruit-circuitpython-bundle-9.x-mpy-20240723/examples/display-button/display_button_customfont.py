# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Button example with a custom font.
"""

import os
import board
import displayio
from adafruit_bitmap_font import bitmap_font
import adafruit_touchscreen
from adafruit_button import Button

# use built in display (MagTag, PyPortal, PyGamer, PyBadge, CLUE, etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

# These pins are used as both analog and digital! XL, XR and YU must be analog
# and digital capable. YD just need to be digital
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(display.width, display.height),
)

# the current working directory (where this file is)
cwd = ("/" + __file__).rsplit("/", 1)[0]
fonts = [
    file
    for file in os.listdir(cwd + "/fonts/")
    if (file.endswith(".bdf") and not file.startswith("._"))
]
for i, filename in enumerate(fonts):
    fonts[i] = cwd + "/fonts/" + filename
print(fonts)
THE_FONT = "/fonts/Arial-12.bdf"
DISPLAY_STRING = "Button Text"

# Make the display context
splash = displayio.Group()
display.root_group = splash
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20

##########################################################################
# Make a background color fill

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x404040
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
print(bg_sprite.x, bg_sprite.y)
splash.append(bg_sprite)

##########################################################################

# Load the font
font = bitmap_font.load_font(THE_FONT)

buttons = []
# Default button styling:
button_0 = Button(
    x=BUTTON_MARGIN,
    y=BUTTON_MARGIN,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="button0",
    label_font=font,
)
buttons.append(button_0)

# a button with no indicators at all
button_1 = Button(
    x=BUTTON_MARGIN * 2 + BUTTON_WIDTH,
    y=BUTTON_MARGIN,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    fill_color=None,
    outline_color=None,
)
buttons.append(button_1)

# various colorings
button_2 = Button(
    x=BUTTON_MARGIN * 3 + 2 * BUTTON_WIDTH,
    y=BUTTON_MARGIN,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="button2",
    label_font=font,
    label_color=0x0000FF,
    fill_color=0x00FF00,
    outline_color=0xFF0000,
)
buttons.append(button_2)

# Transparent button with text
button_3 = Button(
    x=BUTTON_MARGIN,
    y=BUTTON_MARGIN * 2 + BUTTON_HEIGHT,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="button3",
    label_font=font,
    label_color=0x0,
    fill_color=None,
    outline_color=None,
)
buttons.append(button_3)

# a roundrect
button_4 = Button(
    x=BUTTON_MARGIN * 2 + BUTTON_WIDTH,
    y=BUTTON_MARGIN * 2 + BUTTON_HEIGHT,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="button4",
    label_font=font,
    style=Button.ROUNDRECT,
)
buttons.append(button_4)

# a shadowrect
button_5 = Button(
    x=BUTTON_MARGIN * 3 + BUTTON_WIDTH * 2,
    y=BUTTON_MARGIN * 2 + BUTTON_HEIGHT,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="button5",
    label_font=font,
    style=Button.SHADOWRECT,
)
buttons.append(button_5)

# a shadowroundrect
button_6 = Button(
    x=BUTTON_MARGIN,
    y=BUTTON_MARGIN * 3 + BUTTON_HEIGHT * 2,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="button6",
    label_font=font,
    style=Button.SHADOWROUNDRECT,
)
buttons.append(button_6)

for b in buttons:
    splash.append(b)

while True:
    p = ts.touch_point
    if p:
        print(p)
        for i, b in enumerate(buttons):
            if b.contains(p):
                print("Button %d pressed" % i)
                b.selected = True
            else:
                b.selected = False
