# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from rainbowio import colorwheel
import adafruit_pca9685
import adafruit_rgbled

# PCA9685 Initialization
i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 60

# PCA9685 LED Channels
RED_LED = pca.channels[0]
GREEN_LED = pca.channels[1]
BLUE_LED = pca.channels[2]

# Create the RGB LED object
led = adafruit_rgbled.RGBLED(RED_LED, GREEN_LED, BLUE_LED, invert_pwm=True)

# Optionally, you can also create the RGB LED object with inverted PWM
# led = adafruit_rgbled.RGBLED(RED_LED, GREEN_LED, BLUE_LED, invert_pwm=True)


def rainbow_cycle(wait):
    for i in range(255):
        i = (i + 1) % 256
        led.color = colorwheel(i)
        time.sleep(wait)


while True:
    # setting RGB LED color to RGB Tuples (R, G, B)
    print("setting color 1")
    led.color = (255, 0, 0)
    time.sleep(1)

    print("setting color 2")
    led.color = (0, 255, 0)
    time.sleep(1)

    print("setting color 3")
    led.color = (0, 0, 255)
    time.sleep(1)

    # setting RGB LED color to 24-bit integer values
    led.color = 0xFF0000
    time.sleep(1)

    led.color = 0x00FF00
    time.sleep(1)

    led.color = 0x0000FF
    time.sleep(1)

    # rainbow cycle the RGB LED
    rainbow_cycle(0.01)
