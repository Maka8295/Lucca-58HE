# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""If you're using Mu, this example will plot the temperature in C and F on the plotter! Click
"Plotter" to open it, and place your finger over the sensor to see the numbers change. The
sensor is located next to the picture of the thermometer on the CPX."""
import time
from adafruit_circuitplayground import cp

while True:
    print("Temperature C:", cp.temperature)
    print("Temperature F:", cp.temperature * 1.8 + 32)
    print((cp.temperature, cp.temperature * 1.8 + 32))
    time.sleep(0.1)
