# SPDX-FileCopyrightText: 2023 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from micropython import const
from adafruit_seesaw.seesaw import Seesaw

BUTTON_1 = const(3)
BUTTON_2 = const(13)
BUTTON_3 = const(2)
BUTTON_4 = const(14)

JOY1_X = const(1)
JOY1_Y = const(15)
JOY2_X = const(0)
JOY2_Y = const(16)

button_mask = const(
    (1 << BUTTON_1) | (1 << BUTTON_2) | (1 << BUTTON_3) | (1 << BUTTON_4)
)

i2c_bus = board.STEMMA_I2C()  # The built-in STEMMA QT connector on the microcontroller
# i2c_bus = board.I2C()  # Uses board.SCL and board.SDA. Use with breadboard.

seesaw = Seesaw(i2c_bus, addr=0x49)

seesaw.pin_mode_bulk(button_mask, seesaw.INPUT_PULLUP)

last_x = 0
last_y = 0
x = 0
y = 0

while True:
    # These joysticks are really jittery so let's take 4 samples of each axis
    for i in range(4):
        x += seesaw.analog_read(JOY1_X)
        y += seesaw.analog_read(JOY1_Y)

    # take average reading
    x /= 4
    y /= 4

    # PC joysticks aren't true voltage divider because we have a fixed 10K
    # we dont know the normalized value so we're just going to give you
    # the result in 'Kohms' for easier printing

    x = 1024 / x - 1
    y = 1024 / y - 1

    if (abs(x - last_x) > 3) or (abs(y - last_y) > 3):
        print(x, y)
        last_x = x
        last_y = y

    buttons = seesaw.digital_read_bulk(button_mask)

    if not buttons & (1 << BUTTON_1):
        print("Button 1 pressed")

    if not buttons & (1 << BUTTON_2):
        print("Button 2 pressed")

    if not buttons & (1 << BUTTON_3):
        print("Button 3 pressed")

    if not buttons & (1 << BUTTON_4):
        print("Button 4 pressed")

    time.sleep(0.01)
