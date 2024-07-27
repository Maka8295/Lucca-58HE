# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

####### NOTE ################
# This example is meant for use with Blinka/rasberry Pi due to the lack of analog pins.
# CircuitPython board users should run the "ds1841_simpletest.py" example

# WIRING:
# 1 Wire connecting  VCC to RH to make a voltage divider using the
#   internal resistor between RH and RW

# As this code runs, measure the voltage between ground and the RW (wiper) pin
# with a multimeter. You should see the voltage change with each print statement.
from time import sleep
import board
import busio
import adafruit_ds1841

i2c = busio.I2C(board.SCL, board.SDA)
ds1841 = adafruit_ds1841.DS1841(i2c)

while True:
    ds1841.wiper = 127
    print("Wiper value set to 127")
    sleep(5.0)

    ds1841.wiper = 0
    print("Wiper value set to 0")
    sleep(5.0)

    ds1841.wiper = 63
    print("Wiper value set to 63")
    sleep(5.0)
