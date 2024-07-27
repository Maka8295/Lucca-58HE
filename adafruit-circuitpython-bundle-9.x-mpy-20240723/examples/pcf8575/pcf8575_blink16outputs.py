# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import adafruit_pcf8575

print("PCF8575 16 output LED blink test")

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
pcf = adafruit_pcf8575.PCF8575(i2c)

while True:
    pcf.write_gpio(0x5555)  # set every other pin high
    time.sleep(0.2)
    pcf.write_gpio(0xAAAA)  # toggle high/low pins
    time.sleep(0.2)
