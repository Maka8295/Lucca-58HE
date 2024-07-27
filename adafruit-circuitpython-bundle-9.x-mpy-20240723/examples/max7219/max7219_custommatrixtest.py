# SPDX-FileCopyrightText: 2021 Daniel Flanagan
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
from adafruit_max7219 import matrices


# You may need to change the chip select pin depending on your wiring
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D4)

matrix = matrices.CustomMatrix(spi, cs, 32, 8)
while True:
    print("Cycle Start")
    # all lit up
    matrix.fill(True)
    matrix.show()
    time.sleep(0.5)

    # all off
    matrix.fill(False)
    matrix.show()
    time.sleep(0.5)

    # snake across panel
    for y in range(8):
        for x in range(32):
            if not y % 2:
                matrix.pixel(x, y, 1)
            else:
                matrix.pixel(31 - x, y, 1)
            matrix.show()
            time.sleep(0.05)

    # show a string one character at a time
    adafruit = "Adafruit"
    matrix.fill(0)
    for i, char in enumerate(adafruit[:3]):
        matrix.text(char, i * 6, 0)
        matrix.show()
        time.sleep(1.0)
    matrix.fill(0)
    for i, char in enumerate(adafruit[3:]):
        matrix.text(char, i * 6, 0)
        matrix.show()
        time.sleep(1.0)

    # scroll the last character off the display
    for i in range(32):
        matrix.scroll(-1, 0)
        matrix.show()
        time.sleep(0.25)

    # scroll a string across the display
    for pixel_position in range(len(adafruit) * 8):
        matrix.fill(0)
        matrix.text(adafruit, -pixel_position, 0)
        matrix.show()
        time.sleep(0.25)
