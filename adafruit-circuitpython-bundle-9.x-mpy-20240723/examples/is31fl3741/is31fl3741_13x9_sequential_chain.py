# SPDX-FileCopyrightText: 2023 DJDevon3
# SPDX-License-Identifier: MIT
# Chaining 4 13x9 Matrix's to run sequentially (not simultaneously)

import board
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_is31fl3741 import PREFER_BUFFER
from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT
from adafruit_is31fl3741.is31fl3741_pixelbuf import IS31FL3741_PixelBuf

# Initialize I2C Bus
i2c = board.STEMMA_I2C()
# i2c = board.I2C()  # uses board.SCL and board.SDA

# Initialize each 13x9 Matrix
Matrix30 = Adafruit_RGBMatrixQT(i2c, address=0x30, allocate=PREFER_BUFFER)
Matrix30.set_led_scaling(0xFF)
Matrix30.global_current = 0x01
Matrix30.enable = True

Matrix31 = Adafruit_RGBMatrixQT(i2c, address=0x31, allocate=PREFER_BUFFER)
Matrix31.set_led_scaling(0xFF)
Matrix31.global_current = 0x01
Matrix31.enable = True

Matrix32 = Adafruit_RGBMatrixQT(i2c, address=0x32, allocate=PREFER_BUFFER)
Matrix32.set_led_scaling(0xFF)
Matrix32.global_current = 0x01
Matrix32.enable = True

Matrix33 = Adafruit_RGBMatrixQT(i2c, address=0x33, allocate=PREFER_BUFFER)
Matrix33.set_led_scaling(0xFF)
Matrix33.global_current = 0x01
Matrix33.enable = True

# Demo scrolling pixels
WIDTH = 13
HEIGHT = 9
LEDS_MAP = tuple(
    (
        address
        for y in range(HEIGHT)
        for x in range(WIDTH)
        for address in Adafruit_RGBMatrixQT.pixel_addrs(x, y)
    )
)
Matrix30_pixels = IS31FL3741_PixelBuf(Matrix30, LEDS_MAP, init=False, auto_write=False)
Matrix30_chase = RainbowChase(Matrix30_pixels, speed=0.1, size=1, spacing=3, step=8)

Matrix31_pixels = IS31FL3741_PixelBuf(Matrix31, LEDS_MAP, init=False, auto_write=False)
Matrix31_chase = RainbowChase(Matrix31_pixels, speed=0.1, size=1, spacing=3, step=8)

Matrix32_pixels = IS31FL3741_PixelBuf(Matrix32, LEDS_MAP, init=False, auto_write=False)
Matrix32_chase = RainbowChase(Matrix32_pixels, speed=0.1, size=1, spacing=3, step=8)

Matrix33_pixels = IS31FL3741_PixelBuf(Matrix33, LEDS_MAP, init=False, auto_write=False)
Matrix33_chase = RainbowChase(Matrix33_pixels, speed=0.1, size=1, spacing=3, step=8)

# Run animation on each 13x9 matrix sequentially
animations = AnimationSequence(
    Matrix30_chase,
    Matrix31_chase,
    Matrix32_chase,
    Matrix33_chase,
    advance_interval=1,
    auto_clear=False,
)
while True:
    animations.animate()
