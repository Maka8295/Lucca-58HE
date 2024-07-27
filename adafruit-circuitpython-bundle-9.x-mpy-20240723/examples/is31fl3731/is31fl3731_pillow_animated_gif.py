# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example to extract the frames and other parameters from an animated gif
and then run the animation on the display.

Usage:
python3 is31fl3731_pillow_animated_gif.py animated.gif

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import sys
import board
from PIL import Image

# uncomment next line if you are using Adafruit 16x9 Charlieplexed PWM LED Matrix
# from adafruit_is31fl3731.matrix import Matrix as Display
# uncomment next line if you are using Adafruit 16x8 Charlieplexed Bonnet
from adafruit_is31fl3731.charlie_bonnet import CharlieBonnet as Display

# uncomment next line if you are using Pimoroni Scroll Phat HD LED 17 x 7
# from adafruit_is31fl3731.scroll_phat_hd import ScrollPhatHD as Display

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

display = Display(i2c)


# Open the gif
if len(sys.argv) < 2:
    print("No image file specified")
    print("Usage: python3 is31fl3731_pillow_animated_gif.py animated.gif")
    sys.exit()

image = Image.open(sys.argv[1])

# Make sure it's animated
if not image.is_animated:
    print("Specified image is not animated")
    sys.exit()

# Get the autoplay information from the gif
delay = image.info["duration"]

# Figure out the correct loop count
if "loop" in image.info:
    loops = image.info["loop"]
    if loops > 0:
        loops += 1
else:
    loops = 1

# IS31FL3731 only supports 0-7
loops = min(loops, 7)

# Get the frame count (maximum 8 frames)
frame_count = min(image.n_frames, 8)

# Load each frame of the gif onto the Matrix
for frame in range(frame_count):
    image.seek(frame)
    frame_image = Image.new("L", (display.width, display.height))
    frame_image.paste(
        image.convert("L"),
        (
            display.width // 2 - image.width // 2,
            display.height // 2 - image.height // 2,
        ),
    )
    display.image(frame_image, frame=frame)

display.autoplay(delay=delay, loops=loops)
