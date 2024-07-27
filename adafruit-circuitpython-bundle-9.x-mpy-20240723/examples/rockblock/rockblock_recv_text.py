# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=wrong-import-position
import time

# CircuitPython / Blinka
import board

uart = board.UART()
uart.baudrate = 19200

# via USB cable
# import serial
# uart = serial.Serial("/dev/ttyUSB0", 19200)

from adafruit_rockblock import RockBlock

rb = RockBlock(uart)

# try a satellite Short Burst Data transfer
print("Talking to satellite...")
status = rb.satellite_transfer()
# loop as needed
retry = 0
while status[0] > 8:
    time.sleep(10)
    status = rb.satellite_transfer()
    print(retry, status)
    retry += 1
print("\nDONE.")

# get the text
print(rb.text_in)
