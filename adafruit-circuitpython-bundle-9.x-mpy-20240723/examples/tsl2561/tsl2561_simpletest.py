# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_tsl2561

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the TSL2561 instance, passing in the I2C bus
tsl = adafruit_tsl2561.TSL2561(i2c)

# Print chip info
print("Chip ID = {}".format(tsl.chip_id))
print("Enabled = {}".format(tsl.enabled))
print("Gain = {}".format(tsl.gain))
print("Integration time = {}".format(tsl.integration_time))

print("Configuring TSL2561...")

# Enable the light sensor
tsl.enabled = True
time.sleep(1)

# Set gain 0=1x, 1=16x
tsl.gain = 0

# Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)
tsl.integration_time = 1

print("Getting readings...")

# Get raw (luminosity) readings individually
broadband = tsl.broadband
infrared = tsl.infrared

# Get raw (luminosity) readings using tuple unpacking
# broadband, infrared = tsl.luminosity

# Get computed lux value (tsl.lux can return None or a float)
lux = tsl.lux

# Print results
print("Enabled = {}".format(tsl.enabled))
print("Gain = {}".format(tsl.gain))
print("Integration time = {}".format(tsl.integration_time))
print("Broadband = {}".format(broadband))
print("Infrared = {}".format(infrared))
if lux is not None:
    print("Lux = {}".format(lux))
else:
    print("Lux value is None. Possible sensor underrange or overrange.")

# Disble the light sensor (to save power)
tsl.enabled = False
