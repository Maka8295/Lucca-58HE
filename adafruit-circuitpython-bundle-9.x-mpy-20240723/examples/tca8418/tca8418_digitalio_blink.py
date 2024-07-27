# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
from adafruit_tca8418 import TCA8418

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
tca = TCA8418(i2c)

# get a 'digitalio' like pin from the tca
led = tca.get_pin(TCA8418.R0)

# Setup R0 as an output that's at a low logic level default
led.switch_to_output(value=False)

while True:
    led.value = True
    time.sleep(0.2)
    led.value = False
    time.sleep(0.2)
