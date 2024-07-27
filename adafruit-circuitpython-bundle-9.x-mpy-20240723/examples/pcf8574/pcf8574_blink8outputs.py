# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import adafruit_pcf8574

print("PCF8574 8 output LED blink test")

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
pcf = adafruit_pcf8574.PCF8574(i2c)


while True:
    pcf.write_gpio(0x55)  # set every other pun high
    time.sleep(0.2)
    pcf.write_gpio(0xAA)  # toggle high/low pins
    time.sleep(0.2)
