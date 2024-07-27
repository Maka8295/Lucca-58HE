# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from rainbowio import colorwheel
import adafruit_pixie

# For use with CircuitPython:
uart = busio.UART(board.TX, rx=None, baudrate=115200)

# For use on Raspberry Pi/Linux with Adafruit_Blinka:
# import serial
# uart = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3000)

num_pixies = 2  # Change this to the number of Pixie LEDs you have.
pixies = adafruit_pixie.Pixie(uart, num_pixies, brightness=0.2, auto_write=False)


while True:
    for i in range(255):
        for pixie in range(num_pixies):
            pixies[pixie] = colorwheel(i)
        pixies.show()
    time.sleep(2)
    pixies[0] = (0, 255, 0)
    pixies[1] = (0, 0, 255)
    pixies.show()
    time.sleep(1)
    pixies.fill((255, 0, 0))
    pixies.show()
    time.sleep(1)
    pixies[::2] = [(255, 0, 100)] * (2 // 2)
    pixies[1::2] = [(0, 255, 255)] * (2 // 2)
    pixies.show()
    time.sleep(1)
