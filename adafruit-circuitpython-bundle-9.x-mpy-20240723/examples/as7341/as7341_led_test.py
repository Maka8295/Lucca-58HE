# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
from time import sleep
import board
import adafruit_as7341

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_as7341.AS7341(i2c)

print("out of init!")
print("Current current is")
print(sensor.led_current)
print("Setting current")
sensor.led_current = 50
print("enabling led")
sensor.led = True
sleep(0.5)
print("disabling LED")
sensor.led = False

print("led status:", sensor.led)
