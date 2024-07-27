# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example use the temperature sensor on the Circuit Playground, located next to the picture of
the thermometer on the board. Try warming up the board to watch the number of NeoPixels lit up
increase, or cooling it down to see the number decrease. You can set the min and max temperatures
to make it more or less sensitive to temperature changes.
"""
import time
from adafruit_circuitplayground import cp

cp.pixels.auto_write = False
cp.pixels.brightness = 0.3

# Set these based on your ambient temperature in Celsius for best results!
minimum_temp = 24
maximum_temp = 30


def scale_range(value):
    """Scale a value from the range of minimum_temp to maximum_temp (temperature range) to 0-10
    (the number of NeoPixels). Allows remapping temperature value to pixel position."""
    return int((value - minimum_temp) / (maximum_temp - minimum_temp) * 10)


while True:
    peak = scale_range(cp.temperature)
    print(cp.temperature)
    print(int(peak))

    for i in range(10):
        if i <= peak:
            cp.pixels[i] = (0, 255, 255)
        else:
            cp.pixels[i] = (0, 0, 0)
    cp.pixels.show()
    time.sleep(0.05)
