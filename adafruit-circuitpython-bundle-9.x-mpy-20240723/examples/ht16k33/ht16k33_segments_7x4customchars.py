# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
Basic example of setting custom characters on a LED segment display.
"""

# Import all board pins.
import time
import board
import busio
from adafruit_ht16k33 import segments

# Create the character dictionary
# You can use the list normally referenced as a starting point
custom_chars = {}
typical_list_values = segments.NUMBERS
typical_list_chars = list("0123456789abcdef-")
for char, value in zip(typical_list_chars, typical_list_values):
    custom_chars[char] = value

# Add the custom characters you want
custom_chars["s"] = 0b01101101
custom_chars["r"] = 0b01010000
custom_chars["o"] = 0b00111111
custom_chars["l"] = 0b00110000
custom_chars["i"] = 0b00010000
custom_chars["n"] = 0b01010100
custom_chars["g"] = 0b01101111

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
display = segments.Seg7x4(i2c, char_dict=custom_chars)

# Clear the display.
display.fill(0)

# Now you can print custom text
display.print("cool")
time.sleep(3)

# You can also marquee custom text
display.marquee("scrolling... ", 0.2)
