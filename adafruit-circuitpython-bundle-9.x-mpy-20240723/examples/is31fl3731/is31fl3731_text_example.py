# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
import adafruit_framebuf

# uncomment next line if you are using Feather CharlieWing LED 15 x 7
# from adafruit_is31fl3731.charlie_wing import CharlieWing as Display
# uncomment next line if you are using Adafruit 16x9 Charlieplexed PWM LED Matrix
# from adafruit_is31fl3731.matrix import Matrix as Display
# uncomment next line if you are using Adafruit 16x8 Charlieplexed Bonnet
from adafruit_is31fl3731.charlie_bonnet import CharlieBonnet as Display

# uncomment next line if you are using Pimoroni Scroll Phat HD LED 17 x 7
# from adafruit_is31fl3731.scroll_phat_hd import ScrollPhatHD as Display
# uncomment next line if you are using Pimoroni 11x7 LED Matrix Breakout
# from adafruit_is31fl3731.matrix_11x7 import Matrix11x7 as Display

# uncomment this line if you use a Pico, here with SCL=GP21 and SDA=GP20.
# i2c = busio.I2C(board.GP21, board.GP20)

i2c = busio.I2C(board.SCL, board.SDA)

display = Display(i2c)

text_to_show = "Adafruit!!"

# Create a framebuffer for our display
buf = bytearray(32)  # 2 bytes tall x 16 wide = 32 bytes (9 bits is 2 bytes)
fb = adafruit_framebuf.FrameBuffer(
    buf, display.width, display.height, adafruit_framebuf.MVLSB
)


frame = 0  # start with frame 0
while True:
    for i in range(len(text_to_show) * 9):
        fb.fill(0)
        fb.text(text_to_show, -i + display.width, 0, color=1)

        # to improve the display flicker we can use two frame
        # fill the next frame with scrolling text, then
        # show it.
        display.frame(frame, show=False)
        # turn all LEDs off
        display.fill(0)
        for x in range(display.width):
            # using the FrameBuffer text result
            bite = buf[x]
            for y in range(display.height):
                bit = 1 << y & bite
                # if bit > 0 then set the pixel brightness
                if bit:
                    display.pixel(x, y, 50)

        # now that the frame is filled, show it.
        display.frame(frame, show=True)
        frame = 0 if frame else 1
