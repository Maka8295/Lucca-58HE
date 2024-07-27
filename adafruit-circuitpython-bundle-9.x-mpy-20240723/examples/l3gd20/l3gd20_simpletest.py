# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_l3gd20

# Hardware I2C setup:
I2C = board.I2C()  # uses board.SCL and board.SDA
# I2C = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
# Initializes L3GD20 object using default range, 250dps
SENSOR = adafruit_l3gd20.L3GD20_I2C(I2C)
# Initialize L3GD20 object using a custom range and output data rate (ODR).
# SENSOR = adafruit_l3gd20.L3GD20_I2C(
#    I2C, rng=adafruit_l3gd20.L3DS20_RANGE_500DPS, rate=adafruit_l3gd20.L3DS20_RATE_200HZ
# )

# Possible values for rng are:
# adafruit_l3gd20.L3DS20_Range_250DPS, 250 degrees per second. Default range
# adafruit_l3gd20.L3DS20_Range_500DPS, 500 degrees per second
# adafruit_l3gd20.L3DS20_Range_2000DPS, 2000 degrees per second

# Possible values for rate are:
# adafruit_l3gd20.L3DS20_RATE_100HZ, 100Hz data rate. Default data rate
# adafruit_l3gd20.L3DS20_RATE_200HZ, 200Hz data rate
# adafruit_l3gd20.L3DS20_RATE_400HZ, 400Hz data rate
# adafruit_l3gd20.L3DS20_RATE_800HZ, 800Hz data rate

# Hardware SPI setup:
# import digitalio
# CS = digitalio.DigitalInOut(board.D5)
# SPIB = board.SPI()
# SENSOR = adafruit_l3gd20.L3GD20_SPI(SPIB, CS)
# SENSOR = adafruit_l3gd20.L3GD20_I2C(
#    SPIB,
#    CS,
#    rng=adafruit_l3gd20.L3DS20_RANGE_500DPS,
#    rate=adafruit_l3gd20.L3DS20_RATE_200HZ,
# )

while True:
    print("Angular Velocity (rad/s): {}".format(SENSOR.gyro))
    print()
    time.sleep(1)
