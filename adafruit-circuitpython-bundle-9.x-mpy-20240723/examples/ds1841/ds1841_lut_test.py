# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from analogio import AnalogIn
import adafruit_ds1841


# WIRING:
# 1 Wire connecting  VCC to RH to make a voltage divider using the
#   internal resistor between RH and RW
# 2 Wire connecting RW to A0
def wiper_voltage(_wiper_pin):
    raw_value = _wiper_pin.value
    return raw_value / (2**16 - 1) * _wiper_pin.reference_voltage


i2c = busio.I2C(board.SCL, board.SDA)
ds = adafruit_ds1841.DS1841(i2c)


LUT_MAX_INDEX = 71
WIPER_MAX = 127
wiper_pin = AnalogIn(board.A0)

ds.lut_mode_enabled = True

# you only need to run this once per DS1841 since the LUT is stored to EEPROM
# for i in range(0, LUT_MAX_INDEX+1):
#     new_lut_val = WIPER_MAX-i
#     ds.set_lut(i, new_lut_val)

while True:
    for i in range(0, LUT_MAX_INDEX + 1):
        ds.lut_selection = i
        # for printing to serial terminal:
        print(
            "\tLUTAR/LUT Selection: %s" % hex(ds.lut_selection),
            "\tWiper = %d" % ds.wiper,
            "\tWiper Voltage: %f" % wiper_voltage(wiper_pin),
        )
        time.sleep(0.5)

        # uncomment this and comment out the above to print out a mu plotter friendly format (tuple)
        # print((wiper_voltage(wiper_pin),))
