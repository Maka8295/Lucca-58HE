# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Copyright (c) 2017 Adafruit Industries
# Author: James DeVito
# Ported to RGB Display by Melissa LeBlanc-Williams
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
"""
This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT

# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for color.
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Clear display.
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
disp.image(image)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

udlr_fill = "#00FF00"
udlr_outline = "#00FFFF"
button_fill = "#FF00FF"
button_outline = "#FFFFFF"

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

while True:
    up_fill = 0
    if not button_U.value:  # up pressed
        up_fill = udlr_fill
    draw.polygon(
        [(40, 40), (60, 4), (80, 40)], outline=udlr_outline, fill=up_fill
    )  # Up

    down_fill = 0
    if not button_D.value:  # down pressed
        down_fill = udlr_fill
    draw.polygon(
        [(60, 120), (80, 84), (40, 84)], outline=udlr_outline, fill=down_fill
    )  # down

    left_fill = 0
    if not button_L.value:  # left pressed
        left_fill = udlr_fill
    draw.polygon(
        [(0, 60), (36, 42), (36, 81)], outline=udlr_outline, fill=left_fill
    )  # left

    right_fill = 0
    if not button_R.value:  # right pressed
        right_fill = udlr_fill
    draw.polygon(
        [(120, 60), (84, 42), (84, 82)], outline=udlr_outline, fill=right_fill
    )  # right

    center_fill = 0
    if not button_C.value:  # center pressed
        center_fill = button_fill
    draw.rectangle((40, 44, 80, 80), outline=button_outline, fill=center_fill)  # center

    A_fill = 0
    if not button_A.value:  # left pressed
        A_fill = button_fill
    draw.ellipse((140, 80, 180, 120), outline=button_outline, fill=A_fill)  # A button

    B_fill = 0
    if not button_B.value:  # left pressed
        B_fill = button_fill
    draw.ellipse((190, 40, 230, 80), outline=button_outline, fill=B_fill)  # B button

    # make a random color and print text
    rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
    draw.text((20, 150), "Hello World", font=fnt, fill=rcolor)
    rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
    draw.text((20, 180), "Hello World", font=fnt, fill=rcolor)
    rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
    draw.text((20, 210), "Hello World", font=fnt, fill=rcolor)

    # Display the Image
    disp.image(image)

    time.sleep(0.01)
