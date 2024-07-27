# SPDX-FileCopyrightText: Copyright (c) 2020 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import busio
import board
import adafruit_aw9523

i2c = busio.I2C(board.SCL, board.SDA)
aw = adafruit_aw9523.AW9523(i2c)
print("Found AW9523")

# Set all pins to outputs and LED (const current) mode
aw.LED_modes = 0xFFFF
aw.directions = 0xFFFF

n = 0
while True:
    for pin in range(16):
        # every LED is 'offset' by 16 counts so they dont all pulse together
        aw.set_constant_current(pin, (pin * 16 + n) % 256)
    # n increments to increase the current from 0 to 255, then wraps around
    n = (n + 1) % 256
