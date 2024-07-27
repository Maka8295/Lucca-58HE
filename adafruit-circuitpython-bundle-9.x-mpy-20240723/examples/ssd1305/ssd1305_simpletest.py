# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Import all board pins.
from board import SCL, SDA, D4
import busio
import digitalio

# Import the SSD1305 module.
import adafruit_ssd1305

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(D4)

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1305 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
display = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c, addr=0x3C, reset=oled_reset)

# Alternatively you can change the I2C address of the device with an addr parameter:
# display = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c, addr=0x31, reset=oled_reset)

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
display.fill(0)

display.show()

# Set a pixel in the origin 0,0 position.
display.pixel(0, 0, 1)
# Set a pixel in the middle 64, 16 position.
display.pixel(64, 16, 1)
# Set a pixel in the opposite 127, 31 position.
display.pixel(127, 31, 1)
display.show()
