# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio

# uncomment next line if you are using Feather CharlieWing LED 15 x 7
from adafruit_is31fl3731.charlie_wing import CharlieWing as Display

# uncomment next line if you are using Adafruit 16x9 Charlieplexed PWM LED Matrix
# from adafruit_is31fl3731.matrix import Matrix as Display
# uncomment next line if you are using Adafruit 16x8 Charlieplexed Bonnet
# from adafruit_is31fl3731.charlie_bonnet import CharlieBonnet as Display
# uncomment next line if you are using Pimoroni Scroll Phat HD LED 17 x 7
# from adafruit_is31fl3731.scroll_phat_hd import ScrollPhatHD as Display
# uncomment next line if you are using Pimoroni 11x7 LED Matrix Breakout
# from adafruit_is31fl3731.matrix_11x7 import Matrix11x7 as Display

# uncomment this line if you use a Pico, here with SCL=GP21 and SDA=GP20.
# i2c = busio.I2C(board.GP21, board.GP20)

i2c = busio.I2C(board.SCL, board.SDA)

# array pattern in bits; top row-> bottom row, 8 bits in each row
an_arrow = bytearray((0x08, 0x0C, 0xFE, 0xFF, 0xFE, 0x0C, 0x08, 0x00, 0x00))

display = Display(i2c)

offset = (display.width - 8) // 2

# first load the frame with the arrows; moves the an_arrow to the right in each
# frame
display.sleep(True)  # turn display off while updating blink bits
display.fill(0)
for y in range(display.height):
    row = an_arrow[y]
    for x in range(8):
        bit = 1 << (7 - x) & row
        if bit:
            display.pixel(x + offset, y, 50, blink=True)

display.blink(1000)  # ranges from 270 to 2159; smaller the number to faster blink
display.sleep(False)  # turn display on
