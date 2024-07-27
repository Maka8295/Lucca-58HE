# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board
from micropython import const

from adafruit_seesaw.seesaw import Seesaw

BUTTON_RIGHT = const(7)
BUTTON_DOWN = const(4)
BUTTON_LEFT = const(3)
BUTTON_UP = const(2)
BUTTON_SEL = const(11)
BUTTON_A = const(10)
BUTTON_B = const(9)

button_mask = const(
    (1 << BUTTON_RIGHT)
    | (1 << BUTTON_DOWN)
    | (1 << BUTTON_LEFT)
    | (1 << BUTTON_UP)
    | (1 << BUTTON_SEL)
    | (1 << BUTTON_A)
    | (1 << BUTTON_B)
)

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

ss = Seesaw(i2c_bus, 0x5E)

ss.pin_mode_bulk(button_mask, ss.INPUT_PULLUP)

while True:
    buttons = ss.digital_read_bulk(button_mask)
    if not buttons & (1 << BUTTON_RIGHT):
        print("Button RIGHT pressed")

    if not buttons & (1 << BUTTON_DOWN):
        print("Button DOWN pressed")

    if not buttons & (1 << BUTTON_LEFT):
        print("Button LEFT pressed")

    if not buttons & (1 << BUTTON_UP):
        print("Button UP pressed")

    if not buttons & (1 << BUTTON_SEL):
        print("Button SEL pressed")

    if not buttons & (1 << BUTTON_A):
        print("Button A pressed")

    if not buttons & (1 << BUTTON_B):
        print("Button B pressed")

    time.sleep(0.01)
