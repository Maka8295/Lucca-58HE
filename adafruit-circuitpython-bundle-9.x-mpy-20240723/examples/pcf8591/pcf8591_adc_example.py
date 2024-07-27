# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
from adafruit_pcf8591.pcf8591 import PCF8591

################ Read/ADC Example #####################
#
# This example shows how to use a PCF8591 instance to read one of the ADC channels.
#
# Wiring:
# Connect a voltage source to the first ADC channel, in addition to the
# normal power and I2C connections. The voltage level should be between 0V/GND and VCC
#
########################################
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
pcf = PCF8591(i2c)

channel_a = 0
channel_b = 1

while True:
    read_value = pcf.read(channel_a)
    scaled_value = (read_value / 255) * pcf.reference_voltage

    print("Channel: %d %0.2fV" % (channel_a, scaled_value))
    print("")
    time.sleep(0.1)

    read_value = pcf.read(channel_b)
    scaled_value = (read_value / 255) * pcf.reference_voltage

    print("Channel: %d %0.2fV" % (channel_b, scaled_value))
    print("")
    print("*" * 20)
    time.sleep(1)
