# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_lidarlite


# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)

# Default configuration, with only i2c wires
sensor = adafruit_lidarlite.LIDARLite(i2c)

# Optionally, we can pass in a hardware reset pin, or custom config
# import digitalio
# reset = digitalio.DigitalInOut(board.D5)
# sensor = adafruit_lidarlite.LIDARLite(i2c, reset_pin=reset,
#    configuration=adafruit_lidarlite.CONFIG_MAXRANGE)

# If you want to reset, you can do so, note that it can take 10-20 seconds
# for the data to 'normalize' after a reset (and this isnt documented at all)
# sensor.reset()

while True:
    try:
        # We print tuples so you can plot with Mu Plotter
        print((sensor.distance,))
    except RuntimeError as e:
        # If we get a reading error, just print it and keep truckin'
        print(e)
    time.sleep(0.01)  # you can remove this for ultra-fast measurements!
