# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example uses the temperature sensor on the Circuit Playground, located next to the image of
a thermometer on the board. It prints the temperature in both C and F to the serial console. Try
putting your finger over the sensor to see the numbers change!"""
import time
from adafruit_circuitplayground import cp

while True:
    print("Temperature C:", cp.temperature)
    print("Temperature F:", cp.temperature * 1.8 + 32)
    time.sleep(1)
