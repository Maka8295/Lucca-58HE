# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import digitalio
from adafruit_apds9960.apds9960 import APDS9960

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
int_pin = digitalio.DigitalInOut(board.D5)
int_pin.switch_to_input(pull=digitalio.Pull.UP)
apds = APDS9960(i2c)

# set the interrupt threshold to fire when proximity reading goes above 175
apds.proximity_interrupt_threshold = (0, 175)

# assert the interrupt pin when the proximity interrupt is triggered
apds.enable_proximity_interrupt = True

# enable the sensor's proximity engine
apds.enable_proximity = True

while True:
    # print the proximity reading when the interrupt pin goes low
    if not int_pin.value:
        print(apds.proximity)

        # clear the interrupt
        apds.clear_interrupt()
