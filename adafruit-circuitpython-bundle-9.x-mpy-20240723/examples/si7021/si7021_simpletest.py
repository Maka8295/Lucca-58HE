# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Initializes the sensor, gets and prints readings every two seconds.
"""
import time
import board
import adafruit_si7021

# Create library object using our Bus I2C port
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_si7021.SI7021(i2c)

# If you'd like to use the heater, you can uncomment the code below
# and pick a heater level that works for your purposes
#
# sensor.heater_enable = True
# sensor.heater_level = 0  # Use any level from 0 to 15 inclusive

while True:
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    time.sleep(2)
