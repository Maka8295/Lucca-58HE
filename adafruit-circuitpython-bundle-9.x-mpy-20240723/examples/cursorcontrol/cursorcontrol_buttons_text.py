# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import displayio
from adafruit_button import Button
from adafruit_display_text import label
import terminalio
from adafruit_cursorcontrol.cursorcontrol import Cursor
from adafruit_cursorcontrol.cursorcontrol_cursormanager import CursorManager

# Create the display
display = board.DISPLAY

# Create the display context
splash = displayio.Group()

# Use the built-in system font
font = terminalio.FONT

##########################################################################
# Make a background color fill

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x404040
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

##########################################################################

# Set up button/label properties
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20
LBL_HEADER = [100, 20]
LBL_TEXT = [120, 40]

# Resize buttons for small display (PyGamer)
if display.width < 240:
    BUTTON_WIDTH = int(BUTTON_WIDTH / 2)
    BUTTON_HEIGHT = int(BUTTON_HEIGHT / 2)
    BUTTON_MARGIN = int(BUTTON_MARGIN / 2)
    LBL_HEADER[0] -= 75
    LBL_HEADER[1] -= 10
    LBL_TEXT[0] -= 70
    LBL_TEXT[1] += 55

# Create the buttons
buttons = []

button_speed_inc = Button(
    x=BUTTON_MARGIN,
    y=BUTTON_MARGIN + BUTTON_HEIGHT,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="Speed+",
    label_font=font,
)
buttons.append(button_speed_inc)

button_speed_dec = Button(
    x=BUTTON_MARGIN,
    y=BUTTON_MARGIN * 4 + BUTTON_HEIGHT,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="Speed-",
    label_font=font,
)
buttons.append(button_speed_dec)

button_scale_pos = Button(
    x=BUTTON_MARGIN * 3 + 2 * BUTTON_WIDTH,
    y=BUTTON_MARGIN + BUTTON_HEIGHT,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="Scale+",
    label_font=font,
    style=Button.SHADOWRECT,
)
buttons.append(button_scale_pos)

button_scale_neg = Button(
    x=BUTTON_MARGIN * 3 + 2 * BUTTON_WIDTH,
    y=BUTTON_MARGIN * 4 + BUTTON_HEIGHT,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="Scale-",
    label_font=font,
    style=Button.SHADOWRECT,
)
buttons.append(button_scale_neg)

# Show the button
for b in buttons:
    splash.append(b.group)

# Create a text label
text_label = label.Label(
    font, text="CircuitPython Cursor!", color=0x00FF00, x=LBL_HEADER[0], y=LBL_HEADER[1]
)
splash.append(text_label)

text_speed = label.Label(font, color=0x00FF00, x=LBL_TEXT[0], y=LBL_TEXT[1])
splash.append(text_speed)

text_scale = label.Label(font, color=0x00FF00, x=LBL_TEXT[0], y=LBL_TEXT[1] + 20)
splash.append(text_scale)

# initialize the mouse cursor object
mouse_cursor = Cursor(display, display_group=splash)

# initialize the cursormanager
cursor = CursorManager(mouse_cursor)

# show displayio group
display.root_group = splash

prev_btn = None
while True:
    cursor.update()
    if cursor.is_clicked is True:
        for i, b in enumerate(buttons):
            if b.contains((mouse_cursor.x, mouse_cursor.y)):
                b.selected = True
                print("Button %d pressed" % i)
                if i == 0:  # Increase the cursor speed
                    mouse_cursor.speed += 1
                elif i == 1:  # Decrease the cursor speed
                    mouse_cursor.speed -= 1
                if i == 2:  # Increase the cursor scale
                    mouse_cursor.scale += 1
                elif i == 3:  # Decrease the cursor scale
                    mouse_cursor.scale -= 1
                prev_btn = b
    elif prev_btn is not None:
        prev_btn.selected = False
    text_speed.text = "Speed: {0}px".format(mouse_cursor.speed)
    text_scale.text = "Scale: {0}px".format(mouse_cursor.scale)
    time.sleep(0.1)
