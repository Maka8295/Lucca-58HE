# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example to utilize the Python Imaging Library (Pillow) and draw bitmapped text
to 8 frames and then run autoplay on those frames.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import board
from PIL import Image, ImageDraw, ImageFont

# uncomment next line if you are using Adafruit 16x9 Charlieplexed PWM LED Matrix
# from adafruit_is31fl3731.matrix import Matrix as Display
# uncomment next line if you are using Adafruit 16x8 Charlieplexed Bonnet
from adafruit_is31fl3731.charlie_bonnet import CharlieBonnet as Display

# uncomment next line if you are using Pimoroni Scroll Phat HD LED 17 x 7
# from adafruit_is31fl3731.scroll_phat_hd import ScrollPhatHD as Display

BRIGHTNESS = 32  # Brightness can be between 0-255

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

display = Display(i2c)

display.fill(0)

# 256 Color Grayscale Mode
image = Image.new("L", (display.width, display.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

# Load the text in each frame
for x in range(8):
    draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
    draw.text((x + 1, -2), str(x + 1), font=font, fill=BRIGHTNESS)
    display.image(image, frame=x)

display.autoplay(delay=500)
