# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from time import sleep
import board
import busio
from analogio import AnalogIn
import adafruit_ds1841

####### NOTE ################
# this example will not work with Blinka/rasberry Pi due to the lack of analog pins.
# Blinka and Raspberry Pi users should run the "ds1841_blinka_simpletest.py" example

# WIRING:
# 1 Wire connecting  VCC to RH to make a voltage divider using the
#   internal resistor between RH and RW
# 2 Wire connecting RW to A0

# setup of the i2c bus giving the SCL (clock) and SDA (data) pins from the board
i2c = busio.I2C(board.SCL, board.SDA)
# create the ds1841 instance giving the I2C bus we just set up
ds1841 = adafruit_ds1841.DS1841(i2c)

# set up an analog input, selecting the A0 pin
wiper_output = AnalogIn(board.A0)

while True:
    # set th
    ds1841.wiper = 127
    print("Wiper set to %d" % ds1841.wiper)
    voltage = wiper_output.value
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f V" % voltage)
    print("")
    sleep(1.0)

    ds1841.wiper = 0
    print("Wiper set to %d" % ds1841.wiper)
    voltage = wiper_output.value
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f V" % voltage)
    print("")
    sleep(1.0)

    ds1841.wiper = 63
    print("Wiper set to %d" % ds1841.wiper)
    voltage = wiper_output.value
    voltage *= 3.3
    voltage /= 65535
    print("Wiper voltage: %.2f V" % voltage)
    print("")
    sleep(1.0)
