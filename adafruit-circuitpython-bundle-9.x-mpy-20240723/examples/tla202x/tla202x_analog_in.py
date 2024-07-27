# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board

import adafruit_tla202x.tla2024 as TLA
from adafruit_tla202x.analog_in import AnalogIn

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
tla = TLA.TLA2024(i2c)
val_max = (2**15) - 1
pin_0 = AnalogIn(tla, TLA.A0)
pin_1 = AnalogIn(tla, TLA.A1)
pin_2 = AnalogIn(tla, TLA.A2)
pin_3 = AnalogIn(tla, TLA.A3)
analog_ins = [
    pin_0,
    pin_1,
    pin_2,
    pin_3,
]
while True:
    for a_in in analog_ins:
        raw_value = a_in.value
        voltage_reference = a_in.reference_voltage
        scaled_value = (raw_value / val_max) * voltage_reference

        voltage = a_in.voltage
        print("Pin 0 ADC value: %d lsb" % (raw_value))
        print("Pin 0 Reference Voltage: %0.2fV" % (voltage_reference))
        print("Pin 0 Measured Voltage: %0.2fV" % (scaled_value))

        print("")

    print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
    print("")
    time.sleep(1)
