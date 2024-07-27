# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import adafruit_pcf8575

print("PCF8575 16 input button test")

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
pcf = adafruit_pcf8575.PCF8575(i2c)


# turn on all 16 weak pullups
pcf.write_gpio(0xFFFF)

while True:
    vals = pcf.read_gpio()
    for b in range(16):
        if not vals & (1 << b):
            print("button #%d pressed" % b)
    time.sleep(0.01)  # debounce delay
