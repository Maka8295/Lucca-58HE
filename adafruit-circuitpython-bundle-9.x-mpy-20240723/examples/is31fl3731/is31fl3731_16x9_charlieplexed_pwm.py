# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
""" Adafruit 16x9 Charlieplexed PWM LED Matrix Example """
# pylint: disable=import-error
import board
import adafruit_framebuf

from adafruit_is31fl3731.matrix import Matrix as Display

# Uncomment for Pi Pico
# import busio
# i2c = busio.I2C(board.GP21, board.GP20)

i2c = board.STEMMA_I2C()
display = Display(i2c, address=0x74)

PIXEL_ROTATION = 0  # display rotation (0,90,180,270)
PIXEL_BRIGHTNESS = 20  # values (0-255)
PIXEL_BLINK = False  # blink entire display

TEXT = "Hello World!"  # Scrolling marquee text

print(f"Display Dimensions: {display.width}x{display.height}")
print(f"Text: {TEXT}")

# Create a framebuffer for our display
buf = bytearray(32)  # 2 bytes tall x 16 wide = 32 bytes (9 bits is 2 bytes)
buffer = adafruit_framebuf.FrameBuffer(
    buf, display.width, display.height, adafruit_framebuf.MVLSB
)

FRAME = 0  # start with frame 0
while True:
    # Looping marquee
    for i in range(len(TEXT) * 9):
        buffer.fill(0)
        buffer.text(TEXT, -i + display.width, 0, color=1)
        display.frame(FRAME, show=False)
        display.fill(0)
        for x in range(display.width):
            # using the FrameBuffer text result
            bite = buf[x]
            for y in range(display.height):
                bit = 1 << y & bite
                # if bit > 0 then set the pixel brightness
                if bit:
                    display.pixel(
                        x, y, PIXEL_BRIGHTNESS, blink=PIXEL_BLINK, rotate=PIXEL_ROTATION
                    )
