# SPDX-FileCopyrightText: 2022 Tim Cocks for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board
import displayio
import adafruit_touchscreen
import terminalio
from adafruit_button.sprite_button import SpriteButton

# These pins are used as both analog and digital! XL, XR and YU must be analog
# and digital capable. YD just need to be digital
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(board.DISPLAY.width, board.DISPLAY.height),
)

# Make the display context
main_group = displayio.Group()
board.DISPLAY.root_group = main_group

BUTTON_WIDTH = 10 * 16
BUTTON_HEIGHT = 3 * 16
BUTTON_MARGIN = 20

font = terminalio.FONT

buttons = []


button_0 = SpriteButton(
    x=BUTTON_MARGIN,
    y=BUTTON_MARGIN,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="button0",
    label_font=font,
    bmp_path="bmps/gradient_button_0.bmp",
    selected_bmp_path="bmps/gradient_button_1.bmp",
    transparent_index=0,
)

buttons.append(button_0)

for b in buttons:
    main_group.append(b)
while True:
    p = ts.touch_point
    if p:
        print(p)
        for i, b in enumerate(buttons):
            if b.contains(p):
                print("Button %d pressed" % i)
                b.selected = True
                b.label = "pressed"
            else:
                b.selected = False
                b.label = "button0"

    else:
        for i, b in enumerate(buttons):
            if b.selected:
                b.selected = False
                b.label = "button0"
    time.sleep(0.01)
