# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# simple demo of the TLC59711 16-bit 12 channel LED PWM driver.
# Shows the minimal usage - how to set pixel values in a few ways.
# Author: Tony DiCola

import board
import busio

import adafruit_tlc59711

print("tlc59711_simpletest.py")

# Define SPI bus connected to chip.
# You only need the clock and MOSI (output) line to use this chip.
spi = busio.SPI(board.SCK, MOSI=board.MOSI)
pixels = adafruit_tlc59711.TLC59711(spi, pixel_count=16)

# examples how to set the pixels:
# range:
# 0 - 65535
# or
# 0.0 - 1.0
# every pixel needs a color -
# give it just a list or tuple with 3 integer values: R G B

# set all pixels to a very low level
pixels.set_pixel_all((10, 10, 10))

# every chip has 4 Pixels (=RGB-LEDs = 12 Channel)
pixels[0] = (100, 100, 100)
pixels[1] = (0, 0, 100)
pixels[2] = (0.01, 0.0, 0.01)
pixels[3] = (0.1, 0.01, 0.0)
# if you are ready to show your values you have to call
pixels.show()

# there are a bunch of other ways to set pixel.
# have a look at the other examples.
