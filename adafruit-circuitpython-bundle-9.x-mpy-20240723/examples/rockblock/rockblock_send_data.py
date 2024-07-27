# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=wrong-import-position
import time
import struct

# CircuitPython / Blinka
import board

uart = board.UART()
uart.baudrate = 19200

# via USB cable
# import serial
# uart = serial.Serial("/dev/ttyUSB0", 19200)

from adafruit_rockblock import RockBlock

rb = RockBlock(uart)

# create some data
some_int = 2112
some_float = 42.123456789
some_text = "hello world"
text_len = len(some_text)

# create binary data
data = struct.pack("i", some_int)
data += struct.pack("f", some_float)
data += struct.pack("i", len(some_text))
data += struct.pack("{}s".format(text_len), some_text.encode())

# put data in outbound buffer
rb.data_out = data

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
