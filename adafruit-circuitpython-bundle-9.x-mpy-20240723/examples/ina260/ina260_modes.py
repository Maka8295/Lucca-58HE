# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_ina260 import INA260, Mode

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
ina260 = INA260(i2c)

# trigger a sample
ina260.mode = Mode.TRIGGERED
print("Current (one shot #1): %.2f" % (ina260.current))
print("Voltage (one shot #1): %.2f" % (ina260.voltage))
print("Power   (one shot #1): %.2f" % (ina260.power))

# print it again to show it will return the same value
# until triggered again
print("Current (one shot #1 redux): %.2f" % (ina260.current))
print("Voltage (one shot #1 redux): %.2f" % (ina260.voltage))
print("Power   (one shot #1 redux): %.2f" % (ina260.power))

# trigger a second sample
ina260.mode = Mode.TRIGGERED
print("Current (one shot #2): %.2f" % (ina260.current))
print("Voltage (one shot #2): %.2f" % (ina260.voltage))
print("Power   (one shot #2): %.2f" % (ina260.power))

# put the sensor in power-down mode. It will return
# the previous value until a new mode is chosen
ina260.mode = Mode.SHUTDOWN
print("Current (shutdown): %.2f" % (ina260.current))
print("Voltage (shutdown): %.2f" % (ina260.voltage))
print("Power   (shutdown): %.2f" % (ina260.power))

# return the sensor to the default continuous mode
ina260.mode = Mode.CONTINUOUS
while True:
    print("Current (continuous): %.2f" % (ina260.current))
    print("Voltage (continuous): %.2f" % (ina260.voltage))
    print("Power   (continuous): %.2f" % (ina260.power))
    time.sleep(1)
