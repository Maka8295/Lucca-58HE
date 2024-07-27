# SPDX-FileCopyrightText: Copyright (c) 2020 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import busio
import board
import adafruit_aw9523

i2c = busio.I2C(board.SCL, board.SDA)
aw = adafruit_aw9523.AW9523(i2c)
print("Found AW9523")

# Set all pins to outputs
aw.directions = 0xFFFF

while True:
    # write all outputs, flipping each pin on and off
    aw.outputs = 0x5A5A
    time.sleep(0.1)
    aw.outputs = 0xA5A5
    time.sleep(0.1)
