# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import random
import board
import digitalio
from adafruit_max7219 import bcddigits


# You may need to change the chip select pin depending on your wiring
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D4)

leds = bcddigits.BCDDigits(spi, cs, nDigits=8)
while True:
    # clear display and dim 0
    leds.brightness(0)
    leds.clear_all()

    # place 8-digit number on display
    value = 12345678
    leds.show_str(0, "{:8}".format(value))
    leds.show()

    # increase the brightness slowly
    for i in range(16):
        leds.brightness(i)
        time.sleep(0.5)

    leds.brightness(3)

    # show "-HELP-90" on display
    leds.show_str(6, "90")  # show 90 starting at position 6
    leds.set_digit(0, 10)  # show - at position 0
    leds.set_digit(1, 12)  # show H at position 1
    leds.set_digit(2, 11)  # show E at position 2
    leds.set_digit(3, 13)  # show L at position 3
    leds.set_digit(4, 14)  # show P at position 4
    leds.set_digit(5, 10)  # show - at position 5

    leds.show()
    time.sleep(1.0)

    leds.clear_all()
    leds.brightness(5)

    # set the two dots and two 4-digit numbers
    leds.show_dot(2, 1)
    leds.show_dot(6, 1)
    leds.show_str(0, " 72.5")
    leds.show_str(4, "-10.8")

    leds.show()
    time.sleep(1.0)

    leds.brightness(10)
    leds.clear_all()
    # show a 4 character numeric string
    leds.show_str(0, "   0")
    leds.show()
    time.sleep(1.0)

    leds.clear_all()
    # show 0->8
    for digit in range(8):
        leds.set_digit(digit, digit)

    leds.show()
    time.sleep(1.0)

    # show random 8-digit numbers via show_str
    for _ in range(10):
        number = random.uniform(-1.0, 1.0)
        number *= 10000.0
        number_string = "{:9.3f}".format(number)
        leds.clear_all()
        leds.show_str(0, number_string)
        leds.show()
        time.sleep(1.0)

    # show the help string
    leds.clear_all()
    leds.show_help(2)
    leds.show()

    time.sleep(1.0)
