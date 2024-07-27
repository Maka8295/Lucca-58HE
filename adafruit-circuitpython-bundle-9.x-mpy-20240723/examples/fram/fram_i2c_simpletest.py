# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

## Simple Example For CircuitPython/Python I2C FRAM Library

import board
import busio
import adafruit_fram

## Create a FRAM object (default address used).
i2c = busio.I2C(board.SCL, board.SDA)
fram = adafruit_fram.FRAM_I2C(i2c)

## Optional FRAM object with a different I2C address, as well
## as a pin to control the hardware write protection ('WP'
## pin on breakout). 'write_protected()' can be used
## independent of the hardware pin.

# import digitalio
# wp = digitalio.DigitalInOut(board.D10)
# fram = adafruit_fram.FRAM_I2C(i2c,
#                              address=0x53,
#                              wp_pin=wp)

## Write a single-byte value to register address '0'

fram[0] = 1

## Read that byte to ensure a proper write.
## Note: reads return a bytearray

print(fram[0])

## Or write a sequential value, then read the values back.
## Note: reads return a bytearray. Reads also allocate
##       a buffer the size of slice, which may cause
##       problems on memory-constrained platforms.

# values = list(range(100))  # or bytearray or tuple
# fram[0:100] = values
# print(fram[0:100])
