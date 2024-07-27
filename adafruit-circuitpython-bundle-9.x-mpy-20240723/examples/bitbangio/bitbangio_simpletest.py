# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example is for demonstrating how to retrieving the
board ID from a BME280, which is stored in register 0xD0.
It should return a result of [96]
"""

import board
import digitalio
import adafruit_bitbangio as bitbangio

# Change these to the actual connections
SCLK_PIN = board.D6
MOSI_PIN = board.D17
MISO_PIN = board.D18
CS_PIN = board.D5

cs = digitalio.DigitalInOut(CS_PIN)
cs.switch_to_output(value=True)

spi = bitbangio.SPI(SCLK_PIN, MOSI=MOSI_PIN, MISO=MISO_PIN)
cs.value = 0
while not spi.try_lock():
    pass
spi.write([0xD0])
data = [0x00]
spi.readinto(data)
spi.unlock()
cs.value = 1
print("Result is {}".format(data))
