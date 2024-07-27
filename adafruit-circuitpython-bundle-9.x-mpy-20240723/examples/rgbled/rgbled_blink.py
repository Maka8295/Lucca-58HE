# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows how to create a single RGB LED with a specific color channel
# order and blink it.
import time
import board
import adafruit_rgbled

# Configure the setup
RED_LED = board.D5  # Pin the Red LED is connected to
GREEN_LED = board.D6  # Pin the Green LED is connected to
BLUE_LED = board.D7  # Pin the Blue LED is connected to
COLOR = (100, 50, 150)  # color to blink
CLEAR = (0, 0, 0)  # clear (or second color)
DELAY = 0.25  # blink rate in seconds

# Create the RGB LED object
led = adafruit_rgbled.RGBLED(RED_LED, GREEN_LED, BLUE_LED)

# Optionally, you can also create the RGB LED object with inverted PWM
# led = adafruit_rgbled.RGBLED(RED_LED, GREEN_LED, BLUE_LED, invert_pwm=True)

# Loop forever and blink the color
while True:
    led.color = COLOR
    time.sleep(DELAY)
    led.color = CLEAR
    time.sleep(DELAY)
