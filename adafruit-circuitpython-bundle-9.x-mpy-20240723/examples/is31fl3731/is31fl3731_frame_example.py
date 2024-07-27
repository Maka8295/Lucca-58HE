# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
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

# arrow pattern in bits; top row-> bottom row, 8 bits in each row
arrow = bytearray((0x08, 0x0C, 0xFE, 0xFF, 0xFE, 0x0C, 0x08, 0x00, 0x00))

display = Display(i2c)

# first load the frame with the arrows; moves the arrow to the right in each
# frame
display.sleep(True)  # turn display off while frames are updated
for frame in range(display.width - 8):
    display.frame(frame, show=False)
    display.fill(0)
    for y in range(display.height):
        row = arrow[y]
        for x in range(8):
            bit = 1 << (7 - x) & row
            # display the pixel into selected frame with varying intensity
            if bit:
                display.pixel(x + frame, y, frame**2 + 1)
display.sleep(False)
# now tell the display to show the frame one at time
while True:
    for frame in range(8):
        display.frame(frame)
        time.sleep(0.1)
