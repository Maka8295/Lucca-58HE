# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import digitalio
import adafruit_pcf8574

print("PCF8574 digitalio LED + button test")

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
pcf = adafruit_pcf8574.PCF8574(i2c)

# get a 'digitalio' like pin from the pcf
led = pcf.get_pin(7)
button = pcf.get_pin(0)

# Setup pin7 as an output that's at a high logic level default
led.switch_to_output(value=True)
# Setup pin0 as an output that's got a pullup
button.switch_to_input(pull=digitalio.Pull.UP)


while True:
    led.value = button.value
    time.sleep(0.01)  # debounce
