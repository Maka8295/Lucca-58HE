# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo to read ambient light/lux
# and proximity data from VCNL4020 over I2C

import time
import board
import adafruit_vcnl4020

i2c = board.I2C()

# Initialize VCNL4020
sensor = adafruit_vcnl4020.Adafruit_VCNL4020(i2c)

while True:
    print(f"Proximity is: {sensor.proximity}")
    print(f"Ambient is: {sensor.lux}")
    # uncomment print statement below to log to Mu plotter
    # print((sensor.proximity, sensor.lux,))
    time.sleep(0.1)
