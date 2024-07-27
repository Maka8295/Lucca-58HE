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

# get the raw data
data = rb.data_in
print("Raw data = ", data)

# unpack data (see send example)
some_int = struct.unpack("i", data[0:4])[0]
some_float = struct.unpack("f", data[4:8])[0]
text_len = struct.unpack("i", data[8:12])[0]
some_text = struct.unpack("{}s".format(text_len), data[12:])[0]

# turn text into string
some_text = some_text.decode()

# print results
print("some_int   =", some_int)
print("some_float =", some_float)
print("some_text  =", some_text)
