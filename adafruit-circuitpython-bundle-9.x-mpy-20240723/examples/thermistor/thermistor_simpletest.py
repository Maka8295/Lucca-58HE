# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_thermistor

# these values work with the Adafruit CircuitPlayground Express.
# they may work with other thermistors as well, as they're fairly standard,
# though the pin will likely need to change (ie board.A1)
# pylint: disable=no-member
pin = board.TEMPERATURE
resistor = 10000
resistance = 10000
nominal_temp = 25
b_coefficient = 3950

thermistor = adafruit_thermistor.Thermistor(
    pin, resistor, resistance, nominal_temp, b_coefficient
)

# print the temperature in C and F to the serial console every second
while True:
    celsius = thermistor.temperature
    fahrenheit = (celsius * 9 / 5) + 32
    print("== Temperature ==\n{} *C\n{} *F\n".format(celsius, fahrenheit))
    time.sleep(1)
