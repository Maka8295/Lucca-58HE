# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import digitalio
from adafruit_tca8418 import TCA8418

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
tca = TCA8418(i2c)

# get a 'digitalio' like pins from the tca
led = tca.get_pin(TCA8418.R0)
button = tca.get_pin(TCA8418.R1)

# Setup R0 as an output that's at a low logic level default
led.switch_to_output(value=False)
# Setup R1 as an input with pullup
button.switch_to_input(pull=digitalio.Pull.UP)

while True:
    led.value = button.value
    time.sleep(0.01)  # debounce
