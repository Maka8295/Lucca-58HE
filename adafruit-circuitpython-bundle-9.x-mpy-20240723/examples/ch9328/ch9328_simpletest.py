# SPDX-FileCopyrightText: Copyright (c) 2024 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Simple demo to type "Hello World!" and then delete it"""

import time
import board
from adafruit_ch9328.ch9328 import Adafruit_CH9328
from adafruit_ch9328.ch9328_keymap import Keymap

# Initialize UART for the CH9328
# check for Raspberry Pi
# pylint: disable=simplifiable-condition
if "CE0" and "CE1" in dir(board):
    import serial

    uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
# otherwise use busio
else:
    import busio

    uart = busio.UART(board.TX, board.RX, baudrate=9600)
ch9328 = Adafruit_CH9328(uart)

# Wait for 2 seconds
time.sleep(2)
# Sending "Hello World!" as an ASCII character string
ch9328.send_string("Hello World!")
# Wait for 2 seconds
time.sleep(2)

# Send the backspace key 12 times to erase the string
keys = [Keymap.BACKSPACE, 0, 0, 0, 0, 0]  # Keycode for backspace in US mapping
no_keys_pressed = [0, 0, 0, 0, 0, 0]
for _ in range(12):
    ch9328.send_key_press(keys, 0)  # Press
    ch9328.send_key_press(no_keys_pressed, 0)  # Release the key
