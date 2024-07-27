# SPDX-FileCopyrightText: 2019 Tony DiCola, Brennen Bearnes for Adafruit Industries
# SPDX-License-Identifier: MIT

#!/usr/bin/env python3

# Adafruit Raspberry Pi MPR121 Keyboard Example
#
# Allows you to turn touches detected by the MPR121 into key presses on a
# Raspberry Pi.
#
# Dependencies
# ============
#
# Make sure you have the required dependencies by executing the following commands:
#
#   sudo apt-get update
#   sudo apt-get install build-essential python-dev python-pip libudev-dev
#   sudo pip3 install python-uinput
#   sudo pip3 install adafruit-circuitpython-mpr121
#
# Usage
# =====
#
# To use this program you first need to connect the MPR121 board to the Raspberry
# Pi (either connect the HAT directly to the Pi, or wire the I2C pins SCL, SDA to
# the Pi SCL, SDA, VIN to Pi 3.3V, GND to Pi GND).
#
# Next define the mapping of capacitive touch input presses to keyboard
# button presses.  Scroll down to the KEY_MAPPING dictionary definition below
# and adjust the configuration as described in its comments.
#
# Finally run the script as root:
#
#   sudo python3 pi_keyboard.py
#
# Try pressing buttons and you should see key presses made on the Pi!  (Note
# that you need to be logged directly into the Pi to see the keypresses -
# over an SSH or console cable connection, you won't see anything.)
#
# Press Ctrl-C to quit at any time.
#
# Copyright (c) 2014-2019 Adafruit Industries
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

import logging
import subprocess
import time
import board
import busio
import uinput
import adafruit_mpr121

# Define mapping of capacitive touch pin presses to keyboard button presses.

# Each line here should define a dict entry that maps the capacitive touch
# input number to an appropriate key press.
#
# For reference the list of possible uinput.KEY_* values you can specify is
# defined in linux/input.h:
# http://www.cs.fsu.edu/~baker/devices/lxr/http/source/linux/include/linux/input.h?v=2.6.11.8
#
# Make sure a cap touch input is defined only once or else the program will
# fail to run!

KEY_MAPPING = {
    0: uinput.KEY_UP,
    1: uinput.KEY_DOWN,
    2: uinput.KEY_LEFT,
    3: uinput.KEY_RIGHT,
    4: uinput.KEY_B,
    5: uinput.KEY_A,
    6: uinput.KEY_ENTER,
    7: uinput.KEY_SPACE,
}

# Sleep this long between polling for events:
EVENT_WAIT_SLEEP_SECONDS = 0.25

# Uncomment to enable debug message logging (might slow down key detection).
# logging.basicConfig(level=logging.DEBUG)

# Make sure uinput kernel module is loaded.
subprocess.check_call(["modprobe", "uinput"])

# Configure virtual keyboard.
device = uinput.Device(KEY_MAPPING.values())

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 object.
mpr121 = adafruit_mpr121.MPR121(i2c)

# Event loop to wait for pin changes and respond to them.
print("Press Ctrl-C to quit.")
while True:
    # Loop through all defined inputs:
    for pin, key in KEY_MAPPING.items():
        # Call is_touched and pass it then number of the input.  If it's touched
        # it will return True, otherwise it will return False.
        if mpr121[pin].value:
            logging.debug("Input %i touched!", pin)
            logging.debug("Key: %s", key)
            device.emit_click(key)
    time.sleep(
        EVENT_WAIT_SLEEP_SECONDS
    )  # Small delay to keep from spamming output messages.
