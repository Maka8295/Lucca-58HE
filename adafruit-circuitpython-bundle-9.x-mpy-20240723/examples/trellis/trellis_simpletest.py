# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example of turning on LEDs and handling Keypad
# button activity.

# This example uses only one Trellis board, so all loops assume
# a maximum of 16 LEDs (0-15). For use with multiple Trellis boards,
# see the documentation.

import time
import busio
from board import SCL, SDA
from adafruit_trellis import Trellis

# Create the I2C interface
i2c = busio.I2C(SCL, SDA)

# Create a Trellis object
trellis = Trellis(i2c)  # 0x70 when no I2C address is supplied

# 'auto_show' defaults to 'True', so anytime LED states change,
# the changes are automatically sent to the Trellis board. If you
# set 'auto_show' to 'False', you will have to call the 'show()'
# method afterwards to send updates to the Trellis board.

# Turn on every LED
print("Turning all LEDs on...")
trellis.led.fill(True)
time.sleep(2)

# Turn off every LED
print("Turning all LEDs off...")
trellis.led.fill(False)
time.sleep(2)

# Turn on every LED, one at a time
print("Turning on each LED, one at a time...")
for i in range(16):
    trellis.led[i] = True
    time.sleep(0.1)

# Turn off every LED, one at a time
print("Turning off each LED, one at a time...")
for i in range(15, 0, -1):
    trellis.led[i] = False
    time.sleep(0.1)

# Now start reading button activity
# - When a button is depressed (just_pressed),
#   the LED for that button will turn on.
# - When the button is relased (released),
#   the LED will turn off.
# - Any button that is still depressed (pressed_buttons),
#   the LED will remain on.
print("Starting button sensory loop...")
pressed_buttons = set()
while True:
    # Make sure to take a break during each trellis.read_buttons
    # cycle.
    time.sleep(0.1)

    just_pressed, released = trellis.read_buttons()
    for b in just_pressed:
        print("pressed:", b)
        trellis.led[b] = True
    pressed_buttons.update(just_pressed)
    for b in released:
        print("released:", b)
        trellis.led[b] = False
    pressed_buttons.difference_update(released)
    for b in pressed_buttons:
        print("still pressed:", b)
        trellis.led[b] = True
