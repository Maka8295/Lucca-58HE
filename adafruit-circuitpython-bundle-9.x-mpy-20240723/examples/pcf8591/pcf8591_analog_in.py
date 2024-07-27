# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board

import adafruit_pcf8591.pcf8591 as PCF
from adafruit_pcf8591.analog_in import AnalogIn

################ AnalogIn Example #####################
#
# This example shows how to use the AnalogIn class provided
# by the library by creating an AnalogIn instance and using
# it to measure the voltage at the first ADC channel input
#
# Wiring:
# Connect a voltage source to the first ADC channel, in addition to the
# normal power and I2C connections. The voltage level should be between 0V/GND and VCC
#
########################################

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
pcf = PCF.PCF8591(i2c)

pcf_in_0 = AnalogIn(pcf, PCF.A0)
while True:
    raw_value = pcf_in_0.value
    scaled_value = (raw_value / 65535) * pcf_in_0.reference_voltage

    print("Pin 0: %0.2fV" % (scaled_value))
    print("")
    time.sleep(1)
