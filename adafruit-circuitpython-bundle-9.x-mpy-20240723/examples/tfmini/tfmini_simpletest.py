# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board  # comment this out if using pyserial
import busio  # comment this out if using pyserial
import adafruit_tfmini

# Use hardware uart
uart = busio.UART(board.TX, board.RX)

# Or, you can use pyserial on any computer
# import serial
# uart = serial.Serial("/dev/ttyS2", timeout=1)

# Simplest use, connect with the uart bus object
tfmini = adafruit_tfmini.TFmini(uart)

# You can put in 'short' or 'long' distance mode
tfmini.mode = adafruit_tfmini.MODE_SHORT
print("Now in mode", tfmini.mode)

while True:
    print(
        "Distance: %d cm (strength %d, mode %x)"
        % (tfmini.distance, tfmini.strength, tfmini.mode)
    )
    time.sleep(0.1)
