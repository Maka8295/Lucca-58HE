# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple seesaw test for writing PWM outputs
# On the SAMD09 breakout these are pins 5, 6, and 7
# On the ATtiny8x7 breakout these are pins 0, 1, 9, 12, 13
#
# See the seesaw Learn Guide for wiring details.
# For SAMD09:
# https://learn.adafruit.com/adafruit-seesaw-atsamd09-breakout?view=all#circuitpython-wiring-and-test
# For ATtiny8x7:
# https://learn.adafruit.com/adafruit-attiny817-seesaw/pwmout

import time
import board
from adafruit_seesaw import seesaw, pwmout

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
ss = seesaw.Seesaw(i2c)

PWM_PIN = 12  # If desired, change to any valid PWM output!
led = pwmout.PWMOut(ss, PWM_PIN)

delay = 0.01
while True:
    # The API PWM range is 0 to 65535, but we increment by 256 since our
    # resolution is often only 8 bits underneath
    for cycle in range(0, 65535, 256):  #
        led.duty_cycle = cycle
        time.sleep(delay)
    for cycle in range(65534, 0, -256):
        led.duty_cycle = cycle
        time.sleep(delay)
