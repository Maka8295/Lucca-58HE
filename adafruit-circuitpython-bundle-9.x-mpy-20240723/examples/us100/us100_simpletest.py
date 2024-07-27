# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

# For use with a microcontroller:
import board
import busio
import adafruit_us100

uart = busio.UART(board.TX, board.RX, baudrate=9600)

# For use with USB-to-serial cable:
# import serial
# import adafruit_us100
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)

# For use with Raspberry Pi/Linux:
# import serial
# import adafruit_us100
# uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

us100 = adafruit_us100.US100(uart)

while True:
    print("-----")
    print(f"Temperature: {us100.temperature}°C")
    time.sleep(0.5)
    print(f"Distance: {us100.distance} cm")
    time.sleep(0.5)
