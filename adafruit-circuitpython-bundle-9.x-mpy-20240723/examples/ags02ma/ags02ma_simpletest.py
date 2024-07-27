# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import busio
from adafruit_ags02ma import AGS02MA

# MUST connect I2C at 20KHz! Note some processors, like SAMD21 and SAMD51
# do not go that low...but RP2040, ESP32-S2 does
i2c = busio.I2C(board.SCL, board.SDA, frequency=20_000)

ags = AGS02MA(i2c, address=0x1A)

# It is possible to change the I2C address 'semi-permanently' but
# note that you'll need to restart the script after adjusting the address!
# ags.set_address(0x1A)

while True:
    try:
        res = ags.gas_resistance
        print("Gas resistance: %0.1f Kohms" % (res / 1000))
        tvoc = ags.TVOC
        print("TVOC: %d ppb" % tvoc)
    except RuntimeError:
        print("Retrying....")
    time.sleep(1)
