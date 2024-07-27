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

# fmt: off
sweep = [ 1, 2, 3, 4, 6, 8, 10, 15, 20, 30, 40, 60,
    60, 40, 30, 20, 15, 10, 8, 6, 4, 3, 2, 1, ]
# fmt: on

frame = 0

display = Display(i2c)

while True:
    for incr in range(24):
        # to reduce update flicker, use two frames
        # make a frame active, don't show it yet
        display.frame(frame, show=False)
        # fill the display with the next frame
        for x in range(display.width):
            for y in range(display.height):
                display.pixel(x, y, sweep[(x + y + incr) % 24])
        # show the next frame
        display.frame(frame, show=True)
        if frame:
            frame = 0
        else:
            frame = 1
