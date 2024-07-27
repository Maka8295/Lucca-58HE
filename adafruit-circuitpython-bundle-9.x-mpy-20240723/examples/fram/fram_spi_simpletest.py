# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

## Simple Example For CircuitPython/Python SPI FRAM Library

import board
import busio
import digitalio
import adafruit_fram

## Create a FRAM object.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D5)
fram = adafruit_fram.FRAM_SPI(spi, cs)

## Write a single-byte value to register address '0'

fram[0] = 1

## Read that byte to ensure a proper write.
## Note: 'read()' returns a bytearray

print(fram[0])

## Or write a sequential value, then read the values back.
## Note: 'read()' returns a bytearray. It also allocates
##       a buffer the size of 'length', which may cause
##       problems on memory-constrained platforms.

# values = list(range(100))  # or bytearray or tuple
# fram[0:100] = values
# print(fram[0:100])
